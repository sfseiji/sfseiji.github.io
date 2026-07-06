#!/usr/bin/env python3
"""Weekly auto-update of data/publications.json (runs in GitHub Actions).

Finds papers not yet in the curated database and appends them with
``"new": true`` (rendered with a "New" badge on the website):

1. arXiv query au:"Fujimoto_S" — any new paper with Seiji Fujimoto as author.
2. Per-member arXiv queries — member-led (first-author) papers even when
   Seiji is not a co-author. Members and date bounds: data/group_members.yaml.

The curated side (publist_auto on Seiji's Mac, driven by the ADS library
export) regenerates the full file and replaces auto-added entries once a
paper enters the library; unmatched "new" entries are carried over.

No API keys required (arXiv Atom API). Stdlib + PyYAML only.
"""
import json
import re
import sys
import time
import datetime
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PUB_JSON = ROOT / "data" / "publications.json"
MEMBERS_YAML = ROOT / "data" / "group_members.yaml"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "http://export.arxiv.org/api/query"
PI_NAME = "Seiji Fujimoto"


def title_norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def arxiv_id_of(entry_id):
    # http://arxiv.org/abs/2512.11790v1 -> 2512.11790
    m = re.search(r"abs/([0-9.]+?)(v\d+)?$", entry_id)
    return m.group(1) if m else None


def arxiv_query(search_query, max_results=50):
    url = (f"{ARXIV_API}?search_query={urllib.parse.quote(search_query)}"
           f"&sortBy=submittedDate&sortOrder=descending&max_results={max_results}")
    req = urllib.request.Request(url, headers={"User-Agent": "sfseiji-publication-bot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        tree = ET.parse(r)
    out = []
    for e in tree.getroot().findall(f"{ATOM}entry"):
        authors = [a.findtext(f"{ATOM}name", "").strip() for a in e.findall(f"{ATOM}author")]
        out.append({
            "id": e.findtext(f"{ATOM}id", "").strip(),
            "title": re.sub(r"\s+", " ", e.findtext(f"{ATOM}title", "")).strip(),
            "authors": authors,
            "published": e.findtext(f"{ATOM}published", "")[:10],
        })
    time.sleep(3)  # arXiv API courtesy rate limit
    return out


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

    def is_known(e):
        aid = arxiv_id_of(e["id"])
        return (aid in known_arxiv) or (title_norm(e["title"]) in known_titles)

    members = conf.get("members", [])

    def member_of(first_author_name, pub_date):
        for m in members:
            if first_author_name in (m.get("name_variants") or [m["name"]]):
                if pub_date >= str(m.get("since", "1900-01-01")):
                    return m
        return None

    added = []

    # 1) Papers with Seiji Fujimoto as any author
    for e in arxiv_query(conf["pi"].get("arxiv_query", 'au:"Fujimoto_S"')):
        if PI_NAME not in e["authors"] or is_known(e):
            continue
        pos = e["authors"].index(PI_NAME) + 1
        m = member_of(e["authors"][0], e["published"])
        if pos == 1:
            cat, stud, sname = "first", False, None
        else:
            cat = "second_third" if pos <= 3 else "coauthor"
            stud, sname = (True, m["name"]) if m else (False, None)
        added.append(make_entry(e, cat, stud, sname, fuji_pos=pos))
        known_titles.add(title_norm(e["title"]))

    # 2) Member-led papers where Seiji is not a co-author
    for m in members:
        last = m["name"].split()[-1]
        first_initial = m["name"].split()[0][0]
        for e in arxiv_query(f'au:"{last}_{first_initial}"', max_results=25):
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

    if not added:
        print("No new papers found.")
        return

    data["papers"].extend(added)
    data["papers"].sort(key=lambda p: (p["year"] or 0, p["month"] or 0), reverse=True)
    data["stats"]["n_total"] = len(data["papers"])
    data["stats"]["n_student_led"] = sum(1 for p in data["papers"] if p.get("student_led"))
    data["stats"]["n_first_author"] = sum(1 for p in data["papers"] if p.get("category") == "first")
    data["generated"] = datetime.date.today().isoformat()

    PUB_JSON.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"Added {len(added)} new paper(s):")
    for p in added:
        print(f"  - [{p['category']}] {p['title'][:80]}")


if __name__ == "__main__":
    sys.exit(main())
