#!/usr/bin/env python3
"""Weekly auto-update of data/publications.json (runs in GitHub Actions).

Finds papers not yet in the curated database and appends them with
``"new": true`` (rendered with a "New" badge on the website). The source is
OpenAlex (api.openalex.org), queried per person by ORCID and by name:

1. PI papers: any work with Seiji Fujimoto as an author. Student/postdoc
   flags follow the site-wide rule: postdoc first author counts always,
   student first author only when Seiji is 2nd or 3rd author.
2. Member-led papers: works whose first author is a current group member
   (data/group_members.yaml, on/after their `since` date) and that do not
   include Seiji. These are flagged student_led=True.

Why OpenAlex and why both ORCID and name queries (checked 2026-10-10):
- The arXiv API answered GitHub runners with HTTP 429 "Rate exceeded." for
  26+ minutes, so the old arXiv-based scan could not run.
- OpenAlex links authors to ORCIDs with a lag (recent preprints were still
  unlinked 9-15 days after posting), so the ORCID query alone misses the
  newest papers. Name queries fill that gap; they also return namesakes
  (an engineering paper by another Seiji Fujimoto), so name-only matches
  must sit in Physics and Astronomy and must not carry someone else's ORCID.
- Only works with an arXiv id are added. Journal-only records are left to
  the curated ADS layer; this also keeps journal versions of papers that are
  already listed (often under a reworded title) from being added twice.
  On the 180-day calibration set this gave zero duplicate additions and no
  missed new papers.

Guards added after an adversarial review (2026-10-10):
- Membership windows (`since`, `student_until`) use the arXiv posting month,
  not publication_date: records merged with the journal version carry the
  journal date, 1-19 months after arXiv v1.
- New preprints carry no ORCIDs until OpenAlex links them, so a member who
  matches by name only is accepted only with a group co-author or a
  Toronto/Dunlap affiliation; the Utah namesake of Gavin Farley (2607.06777)
  would otherwise get in again. Member-led candidates where Seiji may appear
  as "Fujimoto, S." are held back too, since they would be misfiled as
  papers without him. Held-back papers are reported as warnings and are
  picked up in a later week once OpenAlex has linked the ORCIDs.
- Papers skipped for a similar title are reported, with the matching title.

Each request is retried on 429/5xx, dropped connections, and malformed
responses. A query that still fails is skipped so the others go through;
the script then exits 1 so the run shows as failed, and the workflow still
commits whatever the other queries found. After two failed queries in a row
the rest are skipped, which bounds the run time when OpenAlex is down or the
daily budget is spent.

The curated side (publist_auto on Seiji's Mac, driven by the ADS library
export) regenerates the full file and replaces auto-added entries once a
paper enters the library; unmatched "new" entries are carried over.

Stdlib + PyYAML only. Set OPENALEX_API_KEY to use a free OpenAlex key;
without one the anonymous daily budget applies (about 150 credits per run).
"""
import datetime
import email.utils
import html
import http.client
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PUB_JSON = ROOT / "data" / "publications.json"
MEMBERS_YAML = ROOT / "data" / "group_members.yaml"

OPENALEX_WORKS = "https://api.openalex.org/works"
USER_AGENT = "sfseiji-publication-bot/2.0 (+https://sfseiji.github.io)"
PI_NAME = "Seiji Fujimoto"
PI_ORCID_FALLBACK = "0000-0001-7201-5066"
STUDENT_ROLES = {"phd_student", "grad_student", "undergrad"}
LOOKBACK_DAYS = 180                 # matches the dedup calibration window
ASTRO_FIELD = "Physics and Astronomy"
# Calibrated: known duplicates 0.81-0.89, new papers <= 0.67. Two distinct
# papers already on the site (the ASAGAO proceedings and catalog papers)
# reach 0.72, so the first choice of 0.7 was too low.
TITLE_JACCARD_DUP = 0.75
AUTHOR_CAP = 100                    # OpenAlex keeps only the first 100 authors
GROUP_AFFIL = ("toronto", "dunlap") # corroborates a name-only member match

RETRY_WAITS = (15, 45, 120)         # seconds before attempts 2, 3, 4
RETRY_STATUS = {429, 500, 502, 503, 504}
REQUEST_PAUSE = 1.0                 # seconds between OpenAlex requests
MAX_FAILED_IN_ROW = 2               # then skip the remaining queries


# --------------------------------------------------------------------------
# HTTP
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


def fetch_json(url):
    """GET an OpenAlex list response, retrying transient failures."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    key = os.environ.get("OPENALEX_API_KEY", "").strip()
    if key:
        # a header, not a query parameter, so the key never shows in logged URLs
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(len(RETRY_WAITS) + 1):
        last = attempt == len(RETRY_WAITS)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                doc = json.load(r)
            if not isinstance(doc, dict) or not isinstance(doc.get("results"), list):
                raise ValueError("response is not an OpenAlex list")
            return doc
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
        except (OSError, http.client.HTTPException, ValueError) as err:
            # OSError covers URLError, timeouts, resets, and TLS errors;
            # HTTPException covers RemoteDisconnected and IncompleteRead;
            # ValueError covers truncated or non-JSON bodies.
            if last:
                raise
            wait = RETRY_WAITS[attempt]
            print(f"  {type(err).__name__}: {err}; retry {attempt + 1}/{len(RETRY_WAITS)} in {wait}s")
        time.sleep(wait)


def openalex_query(filter_expr, min_results=0):
    """All works matching an OpenAlex filter (cursor paging)."""
    out, cursor = [], "*"
    while cursor:
        params = {"filter": filter_expr, "per_page": "100", "cursor": cursor}
        doc = fetch_json(f"{OPENALEX_WORKS}?{urllib.parse.urlencode(params, safe=':,|')}")
        out.extend(doc["results"])
        cursor = (doc.get("meta") or {}).get("next_cursor") if doc["results"] else None
        time.sleep(REQUEST_PAUSE)
    if len(out) < min_results:
        raise ValueError(f"expected at least {min_results} result(s), got {len(out)}")
    return out


# --------------------------------------------------------------------------
# normalisation (calibrated against publications.json on 2026-10-10)
GREEK = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
    "ζ": "zeta", "η": "eta", "θ": "theta", "λ": "lambda", "μ": "mu",
    "ν": "nu", "ξ": "xi", "π": "pi", "ρ": "rho", "σ": "sigma", "τ": "tau",
    "φ": "phi", "χ": "chi", "ψ": "psi", "ω": "omega", "Ω": "omega",
    "Λ": "lambda", "Δ": "delta", "Σ": "sigma", "☉": "sun", "⊙": "sun",
}
DROP_CMDS = (
    r"raisebox-?[0-9.]*ex|textasciitilde|mathrm|mathit|mathbf|textrm|textit|"
    r"textbf|rm|it|bf|sim|approx|simeq|lesssim|gtrsim|lsim|gsim|rsim|"
    r"lt|gt|le|ge|leq|geq|star|ast|odot|sun|times|pm|quad|left|right|"
    r"textendash|textemdash|emph|text|mathcal|mathsf|operatorname"
)
ARXIV_NEW = r"\d{4}\.\d{4,5}"
ARXIV_OLD = r"[a-z\-]+(?:\.[A-Z]{2})?/\d{7}"


def clean_title(t):
    """Display form: tags and entities removed, whitespace collapsed."""
    t = html.unescape(t or "")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_norm(t):
    t = html.unescape(t or "")
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("µ", "μ")
    for g, name in GREEK.items():
        t = t.replace(g, " " + name if name == "sun" else name)
    t = re.sub(r"\\text(mu|alpha|beta|lambda)", r"\1", t)
    t = re.sub(r"\\(" + DROP_CMDS + r")(?![a-z])", " ", t)
    t = re.sub(r"\\([a-zA-Z]+)", r"\1", t)
    t = re.sub(r"(?<![a-z])rsim(?![a-z])", " ", t)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def strip_v(x):
    return re.sub(r"v\d+$", "", x)


def arxiv_from_url(u):
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(" + ARXIV_NEW + "|" + ARXIV_OLD + r")(v\d+)?",
                  u or "", re.I)
    return m.group(1) if m else None


def arxiv_from_bibcode(b):
    if not b or "arXiv" not in b:
        return None
    m = re.match(r"^\d{4}arXiv(\d{4})\.?(\d{4,5})[A-Z.]$", b)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def doi_norm(d):
    if not d:
        return None
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d.strip().lower())
    return re.sub(r"/(pdf|epdf|full|abstract|meta|html|fulltext)$", "", d) or None


def arxiv_from_doi(d):
    d = doi_norm(d)
    if d and d.startswith("10.48550/arxiv."):
        return strip_v(d[len("10.48550/arxiv."):])
    return None


def name_tokens(name):
    n = unicodedata.normalize("NFKD", name or "")
    n = "".join(c for c in n if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z]+", " ", n).split()


def name_key(name):
    """Order-insensitive key: 'Fujimoto, Seiji' == 'Seiji Fujimoto'."""
    return " ".join(sorted(name_tokens(name)))


def short_author(full):
    # "Rohan P. Naidu" or "Naidu, Rohan P." -> "Naidu, R. P."
    full = re.sub(r"\s+", " ", full or "").strip()
    if "," in full:
        last, first = (s.strip() for s in full.split(",", 1))
        parts = first.split()
    else:
        parts = full.split()
        if len(parts) < 2:
            return full
        last, parts = parts[-1], parts[:-1]
    return f"{last}, " + " ".join(p[0] + "." for p in parts) if parts else last


def authors_short(authors, max_show=3):
    shown = ", ".join(short_author(a) for a in authors[:max_show])
    return shown + (", et al." if len(authors) > max_show else "")


# --------------------------------------------------------------------------
# OpenAlex records
def bare_orcid(o):
    return (o or "").replace("https://orcid.org/", "") or None


def day_str(v):
    """YAML gives dates as datetime.date; compare everything as YYYY-MM-DD text."""
    return v.isoformat()[:10] if hasattr(v, "isoformat") else str(v)


def posted_date(pub_date, arxiv_ids):
    """Date for membership windows: the arXiv posting date, not a journal date.

    New-style arXiv ids encode the posting month. A publication_date in a
    later month is the journal date of a merged record, so it is replaced by
    the first day of the arXiv month (every `since` in the YAML is a 1st).
    """
    months = sorted(f"20{m.group(1)}-{m.group(2)}"
                    for m in (re.match(r"(\d\d)(\d\d)\.", a) for a in arxiv_ids) if m)
    if not months:
        return pub_date
    if pub_date and pub_date[:7] <= months[0]:
        return pub_date
    return months[0] + "-01"


def parse_work(w):
    """The fields of an OpenAlex work that the scan needs."""
    arx = set()
    for cand in [arxiv_from_doi(w.get("doi"))] + [
            arxiv_from_url(v) or arxiv_from_doi(v)
            for v in (w.get("ids") or {}).values() if isinstance(v, str)]:
        if cand:
            arx.add(strip_v(cand))
    for loc in w.get("locations") or []:
        for u in (loc.get("landing_page_url"), loc.get("pdf_url")):
            x = arxiv_from_url(u)
            if x:
                arx.add(strip_v(x))
        x = arxiv_from_doi(loc.get("doi"))
        if x:
            arx.add(x)
        m = re.search(r"oai:arXiv\.org:(" + ARXIV_NEW + "|" + ARXIV_OLD + ")", loc.get("id") or "", re.I)
        if m:
            arx.add(strip_v(m.group(1)))
    auths = []
    for au in w.get("authorships") or []:
        a = au.get("author") or {}
        auths.append({
            "orcid": bare_orcid(a.get("orcid")),
            "observed": {bare_orcid(o) for o in (a.get("observed_orcids") or []) if o},
            "name": a.get("display_name") or au.get("raw_author_name") or "",
            "raw": au.get("raw_author_name") or "",
            "affil": " ".join(list(au.get("raw_affiliation_strings") or []) +
                              [i.get("display_name") or "" for i in au.get("institutions") or []]).lower(),
        })
    doi = doi_norm(w.get("doi"))
    date = w.get("publication_date") or ""
    return {
        "id": w.get("id"),
        "title": clean_title(w.get("title") or w.get("display_name")),
        "date": date,
        "posted": posted_date(date, arx),
        "doi": None if (doi or "").startswith("10.48550/") else doi,
        "arxiv": sorted(arx),
        "field": (((w.get("primary_topic") or {}).get("field") or {}).get("display_name")),
        "authors": auths,
        "truncated": len(auths) >= AUTHOR_CAP,
    }


def person_forms(p):
    return {name_key(n) for n in [p["name"]] + list(p.get("name_variants") or []) if n}


def find_author(work, person):
    """(index of `person` in the author list, how it matched) or (None, None)."""
    orcid = person.get("orcid")
    if orcid:
        for i, a in enumerate(work["authors"]):
            if a["orcid"] == orcid or orcid in a["observed"]:
                return i, "orcid"
    forms = person_forms(person)
    for i, a in enumerate(work["authors"]):
        if name_key(a["raw"]) in forms or name_key(a["name"]) in forms:
            # a different ORCID on that author record means a namesake
            if a["orcid"] and orcid and a["orcid"] != orcid:
                return None, None
            return i, "name"
    return None, None


def maybe_initials(work, person):
    """True if an author could be `person` written with initials ("Fujimoto, S.")."""
    toks = name_tokens(person["name"])
    first, last = toks[0], toks[-1]
    orcid = person.get("orcid")
    for a in work["authors"]:
        if a["orcid"] and orcid and a["orcid"] != orcid:
            continue
        if any(last in t and first[0] in t for t in (name_tokens(a["raw"]), name_tokens(a["name"]))):
            return True
    return False


def person_queries(person, since):
    flt = f"from_publication_date:{since},type:article|preprint"
    qs = []
    if person.get("orcid"):
        qs.append(("orcid", f"authorships.author.orcid:{person['orcid']},{flt}"))
    seen = set()
    for n in [person["name"]] + list(person.get("name_variants") or []):
        parts = n.split()
        if len(parts) < 2:
            continue
        for form in (n, f"{parts[-1]}, {' '.join(parts[:-1])}"):
            if form.lower() not in seen:
                seen.add(form.lower())
                qs.append(("name", f'raw_author_name.search:"{form}",{flt}'))
    return qs


# --------------------------------------------------------------------------
# site side
def site_index(papers, excluded):
    known = {"arxiv": set(excluded), "doi": set(), "title": set(), "tokens": []}
    for p in papers:
        for a in (arxiv_from_url(p.get("arxiv_url")), arxiv_from_bibcode(p.get("bibcode")),
                  arxiv_from_doi(p.get("doi"))):
            if a:
                known["arxiv"].add(strip_v(a))
        au = p.get("ads_url") or ""
        m = re.search(r"/abs/arXiv:(" + ARXIV_NEW + ")", au)
        if m:
            known["arxiv"].add(m.group(1))
        m = re.search(r"/abs/([^/?#]+)", au)
        if m:
            b = arxiv_from_bibcode(urllib.parse.unquote(m.group(1)))
            if b:
                known["arxiv"].add(b)
        d = doi_norm(p.get("doi"))
        if d:
            known["doi"].add(d)
        add_title(known, p.get("title"))
    return known


def add_title(known, title):
    t = title_norm(title)
    if t:
        known["title"].add(t.replace(" ", ""))
        known["tokens"].append((set(t.split()), clean_title(title)))


def is_known(work, known):
    """Why the work counts as already listed, or None."""
    if any(a in known["arxiv"] for a in work["arxiv"]):
        return "arxiv id"
    if work["doi"] and work["doi"] in known["doi"]:
        return "doi"
    t = title_norm(work["title"])
    if t.replace(" ", "") in known["title"]:
        return "title"
    toks = set(t.split())
    for s, title in known["tokens"]:
        j = jaccard(toks, s)
        if j >= TITLE_JACCARD_DUP:
            return f'title similarity {j:.2f} to "{title[:80]}"'
    return None


def skip_if_known(work, known):
    why = is_known(work, known)
    if why and why.startswith("title similarity"):
        print(f'::notice::Skipped arXiv:{work["arxiv"][0]} "{work["title"][:80]}": {why}')
    return bool(why)


def remember(work, known):
    known["arxiv"].update(work["arxiv"])
    if work["doi"]:
        known["doi"].add(work["doi"])
    add_title(known, work["title"])


def make_entry(work, category, student_led=False, student_name=None, fuji_pos=None):
    aid = work["arxiv"][0]
    # names as printed on the paper; OpenAlex profile names can carry typos
    names = [a["raw"] or a["name"] for a in work["authors"]]
    date = work["date"]
    return {
        "bibcode": None,
        "title": work["title"],
        "authors_short": authors_short(names),
        "first_author": short_author(names[0]) if names else "",
        "fujimoto_position": fuji_pos,
        "n_authors": None if work["truncated"] else len(names),
        "journal": f"arXiv:{aid}",
        "year": int(date[:4]) if date else None,
        "month": int(date[5:7]) if len(date) >= 7 else None,
        "ads_url": f"https://ui.adsabs.harvard.edu/abs/arXiv:{aid}",
        "arxiv_url": f"https://arxiv.org/abs/{aid}",
        "doi": work["doi"], "citations": None,
        "category": category,
        "student_led": student_led,
        "student_name": student_name,
        "preprint": True,
        "new": True, "unverified": True,
    }


# --------------------------------------------------------------------------
def main():
    data = json.loads(PUB_JSON.read_text())
    conf = yaml.safe_load(MEMBERS_YAML.read_text())
    pi = {"name": conf["pi"].get("name", PI_NAME),
          "orcid": str(conf["pi"].get("orcid") or PI_ORCID_FALLBACK),
          "name_variants": conf["pi"].get("name_variants") or []}
    members = [dict(m, orcid=str(m["orcid"]) if m.get("orcid") else None)
               for m in conf.get("members", [])]
    known = site_index(data["papers"], {str(x) for x in (conf.get("exclude_arxiv_ids") or [])})
    since = (datetime.date.today() - datetime.timedelta(days=LOOKBACK_DAYS)).isoformat()

    failed = []
    in_row = [0]                              # consecutive failed queries

    def gather(person, label, is_pi=False):
        """Works for one person, merged across queries; one record per arXiv id."""
        by_id = {}
        for kind, flt in person_queries(person, since):
            if in_row[0] >= MAX_FAILED_IN_ROW:
                print(f"::warning::Skipped OpenAlex {kind} query for {label} "
                      f"after {in_row[0]} failed queries in a row")
                failed.append(f"{label} ({kind}, skipped)")
                continue
            try:
                # the PI's ORCID query always has recent papers; empty means trouble
                need = 1 if (is_pi and kind == "orcid") else 0
                for w in openalex_query(flt, min_results=need):
                    by_id[w.get("id")] = w
                in_row[0] = 0
            except Exception as err:
                in_row[0] += 1
                print(f"::warning::OpenAlex {kind} query for {label} failed: "
                      f"{type(err).__name__}: {err}")
                failed.append(f"{label} ({kind})")
        best = {}
        for w in map(parse_work, by_id.values()):
            if not w["arxiv"] or not w["authors"]:
                continue                      # journal-only records: curated layer
            key = w["arxiv"][0]
            # OpenAlex sometimes keeps two records for one paper, one with a
            # truncated title; keep the fuller one
            if key not in best or (len(w["title"]), len(w["authors"])) > \
                    (len(best[key]["title"]), len(best[key]["authors"])):
                best[key] = w
        return list(best.values())

    def member_of(work, idx):
        for m in members:
            j, _ = find_author(work, m)
            if j == idx and work["posted"] >= day_str(m.get("since", "1900-01-01")):
                return m
        return None

    def trusted(work, how):
        # name-only matches must be astronomy papers (namesakes exist elsewhere)
        return how == "orcid" or work["field"] == ASTRO_FIELD

    def corroborated(work, idx, member):
        """A name-only member match backed by a group affiliation or co-author."""
        if any(k in work["authors"][idx]["affil"] for k in GROUP_AFFIL):
            return True
        return any(find_author(work, o)[0] not in (None, idx) for o in members if o is not member)

    added = []

    # 1) Papers with Seiji Fujimoto as any author.
    for w in sorted(gather(pi, pi["name"], is_pi=True), key=lambda x: x["date"]):
        pos, how = find_author(w, pi)
        if pos is None or not trusted(w, how) or skip_if_known(w, known):
            continue
        pos += 1
        if pos == 1:
            cat, stud, sname = "first", False, None
        else:
            cat = "second_third" if pos <= 3 else "coauthor"
            stud, sname = False, None
            m = member_of(w, 0)
            if m:
                if m.get("role") == "postdoc":
                    stud, sname = True, m["name"]
                elif (m.get("role") in STUDENT_ROLES and pos <= 3
                      and w["posted"] <= day_str(m.get("student_until", "9999-12-31"))):
                    stud, sname = True, m["name"]
        added.append(make_entry(w, cat, stud, sname, fuji_pos=pos))
        remember(w, known)

    # 2) Member-led papers where Seiji is not an author.
    for m in members:
        for w in sorted(gather(m, m["name"]), key=lambda x: x["date"]):
            idx, how = find_author(w, m)
            if idx != 0 or not trusted(w, how):
                continue
            if w["posted"] < day_str(m.get("since", "1900-01-01")):
                continue
            if find_author(w, pi)[0] is not None:
                continue                      # covered by the PI pass
            if skip_if_known(w, known):
                continue
            ref = f'arXiv:{w["arxiv"][0]} ({m["name"]} first author)'
            if maybe_initials(w, pi):
                print(f"::warning::Held back {ref}: an author may be {pi['name']} "
                      f"written with initials; retried weekly until OpenAlex links ORCIDs")
                continue
            if how == "name" and not corroborated(w, idx, m):
                print(f"::warning::Held back {ref}: name match only, with no group "
                      f"co-author or Toronto affiliation; retried weekly until OpenAlex links ORCIDs")
                continue
            added.append(make_entry(w, "member_led", True, m["name"]))
            remember(w, known)

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
            print(f"  - [{p['category']}] {p['journal']} {p['title'][:80]}")
    else:
        print("No new papers found.")

    if failed:
        print(f"::error::{len(failed)} OpenAlex query(ies) failed: "
              f"{', '.join(failed)}. Results from the other queries were kept.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
