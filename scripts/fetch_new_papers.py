#!/usr/bin/env python3
"""Weekly auto-update of data/publications.json (runs in GitHub Actions).

Finds papers not yet in the curated database and appends them with
``"new": true`` (rendered with a "New" badge on the website):

1. arXiv query au:"Fujimoto, Seiji" for any new paper with Seiji Fujimoto
   as author (full-name form; the old au:"Fujimoto_S" form missed most
   papers). The flag applied to these follows the site-wide student/
   postdoc-led rule: postdoc first author counts always, student first
   author only when Seiji is 2nd or 3rd author.
2. Per-member arXiv queries for member-led (first-author) papers, even when
   Seiji is not a co-author. Members and date bounds: data/group_members.yaml.
   These are flagged student_led=True (led by a current group member by
   definition).

The curated side (publist_auto on Seiji's Mac, driven by the ADS library
export) regenerates the full file and replaces auto-added entries once a
paper enters the library; unmatched "new" entries are carried over.

Each arXiv request is retried on 406/429/5xx, dropped connections, and
empty or non-Atom responses, because the API intermittently rejects CI
runners (the 2026-09-19 and 09-26 runs died on an HTTP 406 at the first
query; the cause is unknown and the same code succeeded on 10-03). A query
that still fails is skipped so the others go through; the script then exits
1 so the run shows as failed, and the workflow still commits whatever the
other queries found.

No API keys required (arXiv Atom API). Stdlib + PyYAML only.
"""
import email.utils
import http.client
import json
import os
import re
import sys
import time
import datetime
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PUB_JSON = ROOT / "data" / "publications.json"
MEMBERS_YAML = ROOT / "data" / "group_members.yaml"

ATOM = "{http://www.w3.org/2005/Atom}"
# https directly to skip the http -> https redirect. Not a proven fix: urllib
# carries the same headers across the redirect, so the 406s are unexplained.
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "sfseiji-publication-bot/1.1 (+https://sfseiji.github.io)"
ACCEPT = "application/atom+xml, application/xml;q=0.9, */*;q=0.8"
COURTESY_SLEEP = 3                 # arXiv asks for >= 3 s between requests
RETRY_WAITS = (15, 45, 120)        # seconds before attempts 2, 3, 4
RETRY_STATUS = {406, 429, 500, 502, 503, 504}
PI_NAME = "Seiji Fujimoto"
STUDENT_ROLES = {"phd_student", "grad_student", "undergrad"}


def title_norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def arxiv_id_of(entry_id):
    # http://arxiv.org/abs/2512.11790v1 -> 2512.11790
    m = re.search(r"abs/([0-9.]+?)(v\d+)?$", entry_id)
    return m.group(1) if m else None


def retry_after_seconds(headers):
    """Seconds from a Retry-After header (delta-seconds or HTTP-date), else None."""
    raw = str((headers or {}).get("Retry-After", "") or "").strip()
    try:
        if re.fullmatch(r"[0-9]+", raw):
            return int(raw)
        if raw:
            when = email.utils.parsedate_to_datetime(raw)
            return max(0, int((when - datetime.datetime.now(when.tzinfo)).total_seconds()))
    except (TypeError, ValueError, OverflowError):
        pass
    return None


def describe_http_error(err):
    try:
        body = err.read(300)
    except Exception:
        body = b""
    return f"url={err.url} headers={dict(err.headers or {})} body={body!r}"


def fetch_atom(url, min_entries=0):
    """GET an arXiv Atom feed, retrying the transient failures seen on CI.

    A response that is not an Atom feed, or has fewer than ``min_entries``
    entries, is treated like a transient failure and retried.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": ACCEPT})
    for attempt in range(len(RETRY_WAITS) + 1):
        last = attempt == len(RETRY_WAITS)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                tree = ET.parse(r)
            root = tree.getroot()
            if root.tag != f"{ATOM}feed":
                raise ET.ParseError(f"not an Atom feed (root <{root.tag}>)")
            if len(root.findall(f"{ATOM}entry")) < min_entries:
                raise ET.ParseError(f"feed has fewer than {min_entries} entries")
            return tree
        except urllib.error.HTTPError as err:   # before OSError: HTTPError subclasses it
            if attempt == 0 or last or err.code not in RETRY_STATUS:
                print(f"  HTTP {err.code}: {describe_http_error(err)}")
            if err.code not in RETRY_STATUS or last:
                raise
            wait = RETRY_WAITS[attempt]
            ra = retry_after_seconds(err.headers)
            if ra is not None:
                wait = min(max(wait, ra), 300)
            print(f"  HTTP {err.code}; retry {attempt + 1}/{len(RETRY_WAITS)} in {wait}s")
        except (OSError, http.client.HTTPException, ET.ParseError) as err:
            # OSError covers URLError, timeouts, resets, and TLS errors;
            # HTTPException covers RemoteDisconnected and IncompleteRead.
            if last:
                raise
            wait = RETRY_WAITS[attempt]
            print(f"  {type(err).__name__}: {err}; retry {attempt + 1}/{len(RETRY_WAITS)} in {wait}s")
        time.sleep(wait)


def arxiv_query(search_query, max_results=50, min_entries=0):
    url = (f"{ARXIV_API}?search_query={urllib.parse.quote(search_query)}"
           f"&sortBy=submittedDate&sortOrder=descending&max_results={max_results}")
    tree = fetch_atom(url, min_entries=min_entries)
    out = []
    for e in tree.getroot().findall(f"{ATOM}entry"):
        authors = [a.findtext(f"{ATOM}name", "").strip() for a in e.findall(f"{ATOM}author")]
        out.append({
            "id": e.findtext(f"{ATOM}id", "").strip(),
            "title": re.sub(r"\s+", " ", e.findtext(f"{ATOM}title", "")).strip(),
            "authors": authors,
            "published": e.findtext(f"{ATOM}published", "")[:10],
        })
    return out


def member_query(m):
    """arXiv author query for a member: full-name 'au:"Last, First"' forms
    built from the member name and every name variant, OR-ed together.
    (The old '{last}_{initial}' form matched only a fraction of papers.)"""
    forms = []
    for v in [m["name"]] + list(m.get("name_variants") or []):
        parts = v.split()
        if len(parts) >= 2:
            form = f'{parts[-1]}, {" ".join(parts[:-1])}'
            if form not in forms:
                forms.append(form)
    if not forms:
        forms = [m["name"]]
    return " OR ".join(f'au:"{f}"' for f in forms)


def short_author(full):
    # "Rohan P. Naidu" -> "Naidu, R. P."
    parts = full.split()
    if len(parts) < 2:
        return full
    last = parts[-1]
    initials = " ".join(p[0] + "." for p in parts[:-1])
    return f"{last}, {initials}"


def authors_short(authors, max_show=3):
    shown = ", ".join(short_author(a) for a in authors[:max_show])
    return shown + (", et al." if len(authors) > max_show else "")


def make_entry(e, category, student_led=False, student_name=None, fuji_pos=None):
    aid = arxiv_id_of(e["id"])
    pub = e["published"]
    year = int(pub[:4]) if pub else None
    month = int(pub[5:7]) if pub else None
    return {
        "bibcode": None,
        "title": e["title"],
        "authors_short": authors_short(e["authors"]),
        "first_author": short_author(e["authors"][0]) if e["authors"] else "",
        "fujimoto_position": fuji_pos,
        "n_authors": len(e["authors"]),
        "journal": f"arXiv:{aid}" if aid else "arXiv e-prints",
        "year": year, "month": month,
        "ads_url": f"https://ui.adsabs.harvard.edu/abs/arXiv:{aid}" if aid else None,
        "arxiv_url": f"https://arxiv.org/abs/{aid}" if aid else None,
        "doi": None, "citations": None,
        "category": category,
        "student_led": student_led,
        "student_name": student_name,
        "preprint": True,
        "new": True, "unverified": True,
    }


def main():
    data = json.loads(PUB_JSON.read_text())
    conf = yaml.safe_load(MEMBERS_YAML.read_text())

    known_titles = {title_norm(p["title"]) for p in data["papers"]}
    known_arxiv = set()
    for p in data["papers"]:
        if p.get("arxiv_url"):
            m = re.search(r"abs/([0-9.]+)", p["arxiv_url"])
            if m:
                known_arxiv.add(m.group(1))

    excluded = {str(x) for x in (conf.get("exclude_arxiv_ids") or [])}

    def is_known(e):
        aid = arxiv_id_of(e["id"])
        return (aid in known_arxiv) or (aid in excluded) \
            or (title_norm(e["title"]) in known_titles)

    members = conf.get("members", [])

    def member_of(first_author_name, pub_date):
        for m in members:
            if first_author_name in (m.get("name_variants") or [m["name"]]):
                if pub_date >= str(m.get("since", "1900-01-01")):
                    return m
        return None

    added = []
    failed = []

    def run_query(label, search_query, max_results=50, min_entries=0):
        # One query failing must not drop the results of the others.
        try:
            return arxiv_query(search_query, max_results=max_results, min_entries=min_entries)
        except Exception as err:
            print(f"::warning::arXiv query for {label} failed: {type(err).__name__}: {err}")
            failed.append(label)
            return []
        finally:
            time.sleep(COURTESY_SLEEP)   # also after a failure, so the next query is spaced

    # 1) Papers with Seiji Fujimoto as any author.
    # student_led follows the site rule: postdoc first author counts in any
    # Seiji position; student first author only when Seiji is 2nd/3rd author
    # (and, for student roles, while still within student_until).
    # The PI query returns the latest 50 papers regardless of date, so an empty
    # feed means something went wrong (min_entries=1 makes it retry).
    for e in run_query(PI_NAME, conf["pi"].get("arxiv_query", 'au:"Fujimoto, Seiji"'),
                       min_entries=1):
        if PI_NAME not in e["authors"] or is_known(e):
            continue
        pos = e["authors"].index(PI_NAME) + 1
        m = member_of(e["authors"][0], e["published"])
        if pos == 1:
            cat, stud, sname = "first", False, None
        else:
            cat = "second_third" if pos <= 3 else "coauthor"
            stud, sname = False, None
            if m:
                if m.get("role") == "postdoc":
                    stud, sname = True, m["name"]
                elif (m.get("role") in STUDENT_ROLES and pos <= 3
                      and e["published"] <= str(m.get("student_until", "9999-12-31"))):
                    stud, sname = True, m["name"]
        added.append(make_entry(e, cat, stud, sname, fuji_pos=pos))
        known_titles.add(title_norm(e["title"]))

    # 2) Member-led papers where Seiji is not a co-author. These stay
    # student_led=True: led by a current group member by definition.
    for m in members:
        for e in run_query(m["name"], member_query(m), max_results=25):
            if not e["authors"] or is_known(e):
                continue
            if e["authors"][0] not in (m.get("name_variants") or [m["name"]]):
                continue
            if e["published"] < str(m.get("since", "1900-01-01")):
                continue
            if PI_NAME in e["authors"]:
                continue  # covered by query 1
            added.append(make_entry(e, "member_led", True, m["name"], fuji_pos=None))
            known_titles.add(title_norm(e["title"]))

    if added:
        data["papers"].extend(added)
        data["papers"].sort(key=lambda p: (p["year"] or 0, p["month"] or 0), reverse=True)
        data["stats"]["n_total"] = len(data["papers"])
        data["stats"]["n_student_led"] = sum(1 for p in data["papers"] if p.get("student_led"))
        data["stats"]["n_first_author"] = sum(1 for p in data["papers"] if p.get("category") == "first")
        data["generated"] = datetime.date.today().isoformat()

        # Write via a temp file so a crash mid-write cannot leave a truncated
        # JSON for the commit step to push.
        tmp = PUB_JSON.with_name(PUB_JSON.name + ".tmp")
        tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False))
        os.replace(tmp, PUB_JSON)
        print(f"Added {len(added)} new paper(s):")
        for p in added:
            print(f"  - [{p['category']}] {p['title'][:80]}")
    else:
        print("No new papers found.")

    if failed:
        print(f"::error::{len(failed)} arXiv query(ies) failed: "
              f"{', '.join(failed)}. Results from the other queries were kept.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
