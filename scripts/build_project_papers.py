#!/usr/bin/env python3
"""Paper lists on the project pages (pages/venus.html and friends), weekly.

data/projects.yaml holds the approved papers for each project. This script
1. fills in metadata for every approved paper: title, venue, year, author
   names and count, and ADS link from data/publications.json (the curated,
   ADS-based list, so journal versions replace arXiv versions after the
   monthly update); the fourth author from OpenAlex (publications.json keeps
   three); everything from OpenAlex for papers not in publications.json;
2. rewrites the list between <!-- project-papers:start KEY --> and
   <!-- project-papers:end --> on each page (only when it changed);
3. looks for candidate papers and posts the new ones to one open GitHub
   issue ("Project paper candidates"), together with earlier candidates that
   still wait for a decision. Nothing reaches a page without approval in
   data/projects.yaml.

Candidate sources (the header of data/projects.yaml has the measured
recall): one OpenAlex title/abstract search shared by all projects, an
OpenAlex full-text search for each project's program IDs, and the paper
lists published by the VENUS and GLIMPSE team sites. No ADS or arXiv API.

Resolved metadata and the candidates already reported are kept in
data/project_papers.json, so a failed OpenAlex call falls back to last
week's data instead of dropping authors. After one OpenAlex call fails
(retries exhausted), the remaining OpenAlex calls of the run are skipped.
Exit status is 1 when anything failed; the pages are still rewritten from
whatever was available.

Stdlib + PyYAML only; reuses the OpenAlex helpers of fetch_new_papers.py.
"""
import datetime
import html
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_new_papers as fnp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_YAML = ROOT / "data" / "projects.yaml"
PUB_JSON = ROOT / "data" / "publications.json"
STATE_JSON = ROOT / "data" / "project_papers.json"

SHOW_AUTHORS = 4
BOLD_NAME = "Fujimoto, S."
ADS_ABS = "https://ui.adsabs.harvard.edu/abs/"
OPENALEX_LOCATIONS = "https://api.openalex.org/locations"
GITHUB_API = "https://api.github.com"
ISSUE_TITLE = "Project paper candidates"
MAX_PAGES = 3                       # per search; results are 100 per page
MAX_REPORT = 60                     # candidates per post; the rest wait a week
PENDING_DAYS = 180                  # undecided candidates are re-listed this long
UNASSIGNED = "_unassigned"
SEARCH_FIELDS = ("id,doi,title,display_name,publication_date,type,ids,locations,"
                 "primary_location,authorships,abstract_inverted_index")
START = re.compile(r"^([ \t]*)<!-- project-papers:start (\w+) -->\n", re.M)
END = re.compile(r"^[ \t]*<!-- project-papers:end -->\n", re.M)
# an empty-abstract hit whose title uses the word in its everyday sense
EVERYDAY_TITLE = re.compile(r"\bVenus\b|\bglimpse")
INITIALS = re.compile(r"(?:[A-Z][a-z]{0,2}\.[\s~-]*)+")

# OpenAlex source names -> the abbreviations used in publications.json
VENUE_ABBR = {
    "the astrophysical journal": "ApJ",
    "the astrophysical journal letters": "ApJL",
    "the astrophysical journal supplement series": "ApJS",
    "astronomy and astrophysics": "A&A",
    "astronomy & astrophysics": "A&A",
    "monthly notices of the royal astronomical society": "MNRAS",
    "the astronomical journal": "AJ",
    "publications of the astronomical society of japan": "PASJ",
    "publications of the astronomical society of the pacific": "PASP",
    "nature": "Nature",
    "nature astronomy": "Nature Astronomy",
    "science": "Science",
    "the open journal of astrophysics": "The Open Journal of Astrophysics",
}
GREEK_TEX = {name: ch for ch, name in fnp.GREEK.items() if ch.islower()}
TEX_SYMBOLS = {"star": "⋆", "odot": "⊙", "sun": "⊙", "sim": "~", "gtrsim": "≳", "lesssim": "≲",
               "simeq": "≃", "approx": "≈", "ge": "≥", "geq": "≥", "le": "≤", "leq": "≤"}


class OpenAlexDown(Exception):
    """An earlier OpenAlex call of this run failed; the rest are skipped."""


OA_STATE = {"down": False}


def oa(fn, *args, **kw):
    if OA_STATE["down"]:
        raise OpenAlexDown("skipped after an earlier OpenAlex failure")
    try:
        return fn(*args, **kw)
    except Exception:
        OA_STATE["down"] = True
        raise


# --------------------------------------------------------------------------
# identifiers
def norm_arxiv(v):
    if isinstance(v, float):
        raise ValueError(f"arXiv id {v!r} must be quoted in projects.yaml")
    a = fnp.strip_v(re.sub(r"(?i)^\s*arxiv:\s*", "", str(v).strip()))
    if not re.fullmatch(fnp.ARXIV_NEW, a):
        raise ValueError(f"not a new-style arXiv id: {v!r}")
    return a


def item_ids(item):
    """(arxiv, doi, bibcode) of a projects.yaml item."""
    return (norm_arxiv(item["arxiv"]) if item.get("arxiv") else None,
            fnp.doi_norm(str(item["doi"])) if item.get("doi") else None,
            str(item["bibcode"]).strip() if item.get("bibcode") else None)


def item_key(item):
    a, d, b = item_ids(item)
    return a or d or b


def arxiv_of_pub(p):
    for a in (fnp.arxiv_from_url(p.get("arxiv_url")), fnp.arxiv_from_bibcode(p.get("bibcode"))):
        if a:
            return fnp.strip_v(a)
    m = re.search(r"/abs/arXiv:(" + fnp.ARXIV_NEW + ")", p.get("ads_url") or "")
    return m.group(1) if m else None


def pub_ids(p):
    return {arxiv_of_pub(p), fnp.doi_norm(p.get("doi")), p.get("bibcode")} - {None}


def pub_index(papers):
    idx = {}
    for p in papers:
        for k in pub_ids(p):
            idx.setdefault(k, p)
    return idx


def find_pub(item, pubs_by_id, oa_rec=None):
    for k in item_ids(item):
        if k and k in pubs_by_id:
            return pubs_by_id[k]
    for d in sorted((oa_rec or {}).get("dois") or ()):   # journal record known only by DOI
        if d in pubs_by_id:
            return pubs_by_id[d]
    return None


def validate(conf):
    """Drop malformed items (reported), so one typo cannot stop the run."""
    errors = []
    for key, c in conf.items():
        for field in ("papers", "exclude"):
            good = []
            for it in c.get(field) or []:
                try:
                    if not isinstance(it, dict) or not item_key(it):
                        raise ValueError(f"needs one of arxiv/doi/bibcode: {it!r}")
                    good.append(it)
                except ValueError as err:
                    errors.append(f"{key}.{field}: {err}")
            c[field] = good
    return errors


# --------------------------------------------------------------------------
# text
def title_html(t):
    """Escaped title with the TeX left over from ADS/OpenAlex turned into HTML."""
    t = html.escape(fnp.clean_title(t), quote=False)
    t = re.sub(r"\\raisebox\s*\{?-?[0-9.]*ex\}?\s*\{?\\textasciitilde\}? ?|\\textasciitilde\}? ?", "~", t)
    t = t.replace("$", "")
    t = re.sub(r"\\[,;:! ]", " ", t)
    t = re.sub(r"\{\\(?:rm|sc|it|bf)\s+([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(?:mathrm|textrm|rm|text)\s*\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(?:mathrm|rm)\s*([A-Za-z]+)", r"\1", t)
    t = re.sub(r"\\(?:text)?mu\s*m\b", "μm", t)
    t = t.replace("\\%", "%")
    t = re.sub(r"(?<!-)---(?!-)", "—", t)
    t = re.sub(r"(?<!-)--(?!-)", "–", t)
    t = re.sub(r"\\([A-Za-z]+)(?![A-Za-z])",
               lambda m: TEX_SYMBOLS.get(m.group(1)) or GREEK_TEX.get(m.group(1)) or m.group(0), t)
    t = t.replace("☉", "⊙")
    tok = r"[0-9.+-]+|[A-Za-z]+|⋆|⊙|\*|\[[^\]]*\]"     # L_[CII] too
    t = re.sub(r"\^\{([^}]*)\}|\^(" + tok + ")", lambda m: f"<sup>{m.group(1) or m.group(2)}</sup>", t)
    t = re.sub(r"_\{([^}]*)\}|_(" + tok + ")", lambda m: f"<sub>{m.group(1) or m.group(2)}</sub>", t)
    t = t.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", t).strip()


def authors_html(shown, n_total):
    """`shown` holds display names already in "Last, I." form."""
    parts = [f"<b>{html.escape(s, quote=False)}</b>" if s == BOLD_NAME else html.escape(s, quote=False)
             for s in shown]
    more = n_total is None or n_total > len(shown)
    return ", ".join(parts) + (", et al." if more else "")


def short_list_from_pub(p):
    """Display names from publications.json authors_short ("Last, I., Last, I. J., et al.").

    Names are "Last, Initials" pairs; a surname not followed by initials
    (a mononym such as "Abdurro'uf", written "Abdurro'uf,,") stands alone."""
    s = re.sub(r",?\s*et al\.?\s*$", "", p.get("authors_short") or "")
    toks = [t.strip() for t in s.split(",")]
    out, i = [], 0
    while i < len(toks):
        if not toks[i]:
            i += 1
            continue
        nxt = toks[i + 1] if i + 1 < len(toks) else ""
        if nxt and INITIALS.fullmatch(nxt):
            out.append(f"{toks[i]}, {nxt.replace('~', ' ')}")
            i += 2
        else:
            out.append(toks[i])
            i += 1
    return out


def surname_tokens(name):
    n = unicodedata.normalize("NFKD", name.split(",")[0] if "," in name else name)
    return set(re.sub(r"[^a-z]+", " ", "".join(c for c in n if not unicodedata.combining(c)).lower()).split())


def venue_text(meta):
    j = meta.get("journal")
    if j and not j.startswith(("arXiv", "Submitted")):
        return f'{j} ({meta.get("year")}).'
    a = meta.get("arxiv")
    if a:
        yr = f"20{a[:2]}" if re.fullmatch(fnp.ARXIV_NEW, a) else meta.get("year")
        return f"arXiv:{a} ({yr})."
    return f'{j} ({meta.get("year")}).' if j else (f'({meta["year"]}).' if meta.get("year") else "")


def ads_link(meta):
    if meta.get("ads_url"):
        return meta["ads_url"].replace("&", "%26")
    if meta.get("arxiv"):
        return f'{ADS_ABS}arXiv:{meta["arxiv"]}'
    if meta.get("doi"):
        return f'{ADS_ABS}{meta["doi"]}'
    return None


def render_list(entries, indent):
    i1, i2, i3 = indent, indent + "  ", indent + "    "
    out = [f'{i1}<ul class="list-group" style="background:transparent;">']
    for n, m in zip(range(len(entries), 0, -1), entries):
        link = ads_link(m)
        out += [f'{i2}<li class="list-group-item">',
                f"{i3}<b>{n}.</b>",
                f"{i3}{authors_html(m['authors'], m.get('n_authors'))}",
                f"{i3}&ldquo;{title_html(m['title'])},&rdquo;"]
        v = venue_text(m)
        if v:
            out.append(f"{i3}{html.escape(v, quote=False)}")
        if link:
            out.append(f'{i3}<a href="{html.escape(link)}" target="_blank">[ADS]</a>')
        out.append(f"{i2}</li>")
    out.append(f"{i1}</ul>")
    return "\n".join(out) + "\n"


def rewrite_page(path, key, entries):
    s = path.read_text()
    starts = [m for m in START.finditer(s) if m.group(2) == key]
    if len(starts) != 1:
        raise ValueError(f"{path}: expected one start marker for '{key}', found {len(starts)}")
    st = starts[0]
    note = re.match(r"[ \t]*<!-- Generated by [^\n]*-->\n", s[st.end():])
    body_start = st.end() + (note.end() if note else 0)
    en = END.search(s, body_start)
    if not en:
        raise ValueError(f"{path}: no end marker after '{key}'")
    new = s[:body_start] + render_list(entries, st.group(1)) + s[en.start():]
    if new != s:
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(new)
        os.replace(tmp, path)
        return True
    return False


# --------------------------------------------------------------------------
# metadata
def is_journal_record(w):
    src = (w.get("primary_location") or {}).get("source") or {}
    return w.get("type") == "article" and src.get("type") == "journal"


def record_dois(w):
    out = {fnp.doi_norm(w.get("doi"))}
    for loc in w.get("locations") or []:
        out.add(fnp.doi_norm(loc.get("doi")))
        lp = loc.get("landing_page_url") or ""
        if "doi.org/" in lp:
            out.add(fnp.doi_norm(lp))
    return {d for d in out if d and not d.startswith("10.48550/")}


def merge_records(found, key, w):
    """Several OpenAlex records can describe one paper (preprint, journal,
    repository copies). Authors come from the best-ranked record; the title
    is the longest seen (journal records sometimes carry a truncated one)."""
    pw = fnp.parse_work(w)
    rank = (len(pw["authors"]) >= SHOW_AUTHORS, is_journal_record(w), len(pw["authors"]))
    old = found.get(key)
    if old is None or rank > old["rank"]:
        rec = dict(pw, rank=rank, journal_record=rank[1],
                   source=((w.get("primary_location") or {}).get("source") or {}),
                   biblio=w.get("biblio") or {})
        rec["dois"] = record_dois(w) | ((old or {}).get("dois") or set())
        rec["long_title"] = max((old or {}).get("long_title") or "", pw["title"], key=len)
        found[key] = rec
    else:
        old["dois"] |= record_dois(w)
        old["long_title"] = max(old.get("long_title") or "", pw["title"], key=len)


def openalex_lookup(items, pubs_by_id):
    """OpenAlex records for the approved papers, keyed by item key.

    One `doi:` filter with every arXiv DOI and every journal DOI known from
    publications.json; the filter also matches DOIs on locations, so merged
    preprint+journal records are found either way. arXiv papers still
    missing (their arXiv DOI can sit on a record that list queries hide) are
    looked up through their arXiv location, one entity request each."""
    want = {}
    for it in items:
        a, d, _ = item_ids(it)
        p = find_pub(it, pubs_by_id) or {}
        want[item_key(it)] = (a, {x for x in (d, fnp.doi_norm(p.get("doi"))) if x})
    dois = sorted({f"10.48550/arxiv.{a}" for a, _ in want.values() if a}
                  | {x for _, ds in want.values() for x in ds})
    found = {}
    for i in range(0, len(dois), 50):
        for w in oa(fnp.openalex_query, "doi:" + "|".join(dois[i:i + 50])):
            pw = fnp.parse_work(w)
            wd = record_dois(w) | ({pw["doi"]} if pw["doi"] else set())
            for k, (a, ds) in want.items():
                if (a and a in pw["arxiv"]) or (ds & wd):
                    merge_records(found, k, w)
    missing = [(k, a) for k, (a, _) in want.items() if a and k not in found]
    for i in range(0, len(missing), 25):
        chunk = missing[i:i + 25]
        flt = "|".join(f"oai:arXiv.org:{a}" for _, a in chunk)
        doc = oa(fnp.fetch_json, OPENALEX_LOCATIONS + "?"
                 + urllib.parse.urlencode({"filter": f"native_id:{flt}", "per_page": "100"}, safe=":,|"))
        for loc in doc["results"]:
            wid = (loc.get("work_id") or "").rsplit("/", 1)[-1]
            a = (loc.get("native_id") or "").rsplit(":", 1)[-1]
            k = next((k for k, aa in chunk if aa == a), None)
            if not (wid and k):
                continue
            merge_records(found, k, oa(fnp.fetch_json, f"{fnp.OPENALEX_WORKS}/{wid}", expect_list=False))
            time.sleep(fnp.REQUEST_PAUSE)
    return found


def names_for(pub, oa_rec):
    """First four display names. publications.json has ADS names for three
    of them; OpenAlex supplies the fourth when its first three are the same
    people (their raw names can differ in form, so surnames are compared)."""
    oa_names = [fnp.short_author(x["raw"] or x["name"]) for x in (oa_rec or {}).get("authors") or []]
    if not pub:
        return oa_names[:SHOW_AUTHORS]
    names = short_list_from_pub(pub)[:SHOW_AUTHORS]
    if len(names) == 3 and len(oa_names) >= SHOW_AUTHORS and all(
            surname_tokens(a) & surname_tokens(b) for a, b in zip(names, oa_names[:3])):
        names.append(oa_names[3])
    return names


def meta_for(item, pub, oa_rec, cached):
    a, d, b = item_ids(item)
    m = {"key": item_key(item), "arxiv": a or (arxiv_of_pub(pub) if pub else None)}
    if pub:
        m.update(title=pub["title"], journal=pub.get("journal"), year=pub.get("year"),
                 ads_url=pub.get("ads_url"), doi=pub.get("doi"))
    elif oa_rec:
        src = (oa_rec["source"].get("display_name") or "").strip()
        bib = oa_rec["biblio"]
        journal = None
        if oa_rec["journal_record"] and src and bib.get("volume"):
            journal = ", ".join(x for x in (VENUE_ABBR.get(src.lower(), src), bib.get("volume"),
                                            bib.get("first_page")) if x)
        m.update(title=oa_rec.get("long_title") or oa_rec["title"], journal=journal,
                 year=int(oa_rec["date"][:4]) if oa_rec["date"] else None,
                 ads_url=None, doi=oa_rec["doi"] or d)
    elif cached:
        m.update({k: cached.get(k) for k in ("title", "journal", "year", "ads_url", "doi")})
    else:
        return None
    if oa_rec or pub:
        names = names_for(pub, oa_rec)
        if len(names) < SHOW_AUTHORS and cached and len(cached.get("authors") or []) > len(names):
            names = cached["authors"]                # keep last week's fourth author
        m["authors"] = names
        m["n_authors"] = (pub or {}).get("n_authors") or (
            (None if oa_rec["truncated"] else len(oa_rec["authors"])) if oa_rec else None)
    else:
        m["authors"], m["n_authors"] = cached.get("authors") or [], cached.get("n_authors")
    m["authors"] = m["authors"][:SHOW_AUTHORS]
    return m


def sort_key(m):
    # newest first by arXiv posting order; papers without an arXiv id by year
    return (m["arxiv"] or f'{(m.get("year") or 0) % 100:02d}99.99999', m["key"])


# --------------------------------------------------------------------------
# candidates
def reconstruct_abstract(inv):
    if not inv:
        return ""
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos)


def mostly_upper(s):
    letters = [c for c in s if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.5


def works_search(params):
    """Cursor-paged /works call with any parameters, capped at MAX_PAGES."""
    out, cursor, doc = [], "*", {}
    for _ in range(MAX_PAGES):
        q = dict(params, per_page="100", cursor=cursor, select=SEARCH_FIELDS)
        doc = oa(fnp.fetch_json, f"{fnp.OPENALEX_WORKS}?{urllib.parse.urlencode(q, safe=':,|')}")
        out.extend(doc["results"])
        cursor = (doc.get("meta") or {}).get("next_cursor") if doc["results"] else None
        time.sleep(fnp.REQUEST_PAUSE)
        if not cursor:
            return out
    print(f"::warning::OpenAlex search stopped at {len(out)} of "
          f"{(doc.get('meta') or {}).get('count')} results ({params})")
    return out


def as_candidate(w, why):
    pw = fnp.parse_work(w)
    if not pw["arxiv"]:
        return None                         # cranks and journal twins
    first = pw["authors"][0] if pw["authors"] else {}
    return {"arxiv": pw["arxiv"][0], "doi": pw["doi"], "title": pw["title"],
            "first_author": fnp.short_author(first.get("raw") or first.get("name") or ""),
            "date": pw["posted"], "why": why}


def match_rules(text, rules):
    for r in rules or []:
        if not re.search(r["pattern"], text):
            continue
        if r.get("require") and not re.search(r["require"], text):
            continue
        if r.get("reject") and re.search(r["reject"], text):
            continue
        return r["why"]
    return None


def search_candidates(conf, det):
    """The shared title/abstract search, split into projects by `match` rules."""
    since = (datetime.date.today() - datetime.timedelta(days=int(det.get("search_days", 60)))).isoformat()
    works = works_search({"search.title_and_abstract": " ".join(det["search"].split()),
                          "filter": f"from_publication_date:{since},type:article|preprint,"
                                    f"primary_topic.field.id:31"})
    out, unmatched = {}, 0
    for w in works:
        title = w.get("title") or w.get("display_name") or ""
        abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
        text = f"{title} {abstract}"
        # all-caps abstracts are cranks; titles and short texts are acronym-heavy anyway
        if len(abstract.split()) >= 20 and mostly_upper(abstract):
            continue
        hits = {k: match_rules(text, (c.get("detect") or {}).get("match")) for k, c in conf.items()}
        hits = {k: v for k, v in hits.items() if v}
        if not hits and not abstract and not EVERYDAY_TITLE.search(title):
            # OpenAlex withholds some publisher abstracts but still searches them
            hits = {UNASSIGNED: "matched the search, but OpenAlex has no abstract to check"}
        if not hits:
            unmatched += 1
        for k, why in hits.items():
            c = as_candidate(w, why)
            if c:
                out.setdefault(k, []).append(c)
    print(f"title/abstract search: {len(works)} hit(s), {unmatched} matched no project rule")
    return out


def fulltext_candidates(phrases, days):
    since = (datetime.date.today() - datetime.timedelta(days=int(days))).isoformat()
    works = works_search({"filter": f"fulltext.search:({phrases}),from_publication_date:{since},"
                                    f"type:article|preprint,primary_topic.subfield.id:3103"})
    ids = sorted(set(re.findall(r"\b\d{4,5}\b", phrases)))
    why = f"full text mentions program {' or '.join(ids)} (may be a citation only)"
    return [c for c in (as_candidate(w, why) for w in works) if c]


def fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": fnp.USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def feed_candidates(feed):
    """Papers listed on a team site's own paper list (a static JSON file)."""
    doc = fetch_feed(feed["url"])
    rows = doc.get("publications") if isinstance(doc, dict) else doc
    if not isinstance(rows, list):
        raise ValueError("unexpected feed format")
    out = []
    for r in rows:
        dt = (r.get("doctype") or "").lower()
        if (dt and dt not in ("article", "eprint")) or re.search(r"\.prop\.|^\d{4}AAS\.", r.get("bibcode") or ""):
            continue                        # proposals, meeting abstracts, errata
        aid = (r.get("arxiv") or fnp.arxiv_from_url(r.get("arxiv_url"))
               or fnp.arxiv_from_bibcode(r.get("bibcode")))
        doi = fnp.doi_norm(r.get("doi") or r.get("doi_url"))
        if not (aid or doi or r.get("bibcode")):
            continue
        authors = r.get("authors") or []
        out.append({"arxiv": fnp.strip_v(str(aid)) if aid else None, "bibcode": r.get("bibcode"),
                    "doi": doi, "title": fnp.clean_title(r.get("title")),
                    "first_author": fnp.short_author(authors[0]) if authors else "",
                    "date": r.get("date") or str(r.get("year") or ""), "why": feed["why"]})
    return out


def cand_ids(c, pubs_by_id):
    ids = {c.get("arxiv"), c.get("bibcode"), c.get("doi")} - {None}
    for i in list(ids):
        if i in pubs_by_id:                 # the same paper under another id
            ids |= pub_ids(pubs_by_id[i])
    return ids


# --------------------------------------------------------------------------
# GitHub issue
def md(s):
    """Third-party text in markdown: no links, emphasis, mentions, or HTML."""
    s = re.sub(r"([\\`*_\[\]()<>#!|~])", r"\\\1", str(s or ""))
    return s.replace("@", "@\u200b")


def github(method, path, payload=None):
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    req = urllib.request.Request(
        f"{GITHUB_API}/repos/{repo}{path}", method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "User-Agent": fnp.USER_AGENT, "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def post_candidates(body):
    """Comment on the open candidates issue, or open one. Returns its URL,
    or None when no token is available (local runs)."""
    if not (os.environ.get("GITHUB_TOKEN") and os.environ.get("GITHUB_REPOSITORY")):
        print("(no GITHUB_TOKEN/GITHUB_REPOSITORY: nothing posted)\n" + body)
        return None
    try:
        open_issues = github("GET", "/issues?state=open&per_page=100&creator="
                             + urllib.parse.quote("github-actions[bot]"))
        issue = next((i for i in open_issues
                      if i.get("title") == ISSUE_TITLE and not i.get("pull_request")), None)
    except (urllib.error.URLError, OSError, ValueError) as err:
        print(f"::warning::could not list issues ({type(err).__name__}: {err}); opening a new one")
        issue = None
    if issue:
        return github("POST", f"/issues/{issue['number']}/comments", {"body": body}).get("html_url")
    return github("POST", "/issues", {"title": ISSUE_TITLE, "body": body}).get("html_url")


def cand_line(c):
    if c.get("arxiv"):
        ident, url, yml = f"arXiv:{c['arxiv']}", f"https://arxiv.org/abs/{c['arxiv']}", f'- arxiv: "{c["arxiv"]}"'
    elif c.get("doi"):
        ident, url, yml = f"doi:{c['doi']}", f"https://doi.org/{c['doi']}", f'- doi: "{c["doi"]}"'
    else:
        ident, url = c.get("bibcode"), f"{ADS_ABS}{urllib.parse.quote(c.get('bibcode') or '')}"
        yml = f'- bibcode: "{c.get("bibcode")}"'
    why = "; ".join(c["why"]) if isinstance(c["why"], list) else c["why"]
    return (f"- [{ident}]({url}) {md(c.get('first_author'))}: {md(c.get('title'))}  \n"
            f"  why: {md(why)}. yaml: `{yml}`")


def section_title(key, conf):
    if key == UNASSIGNED:
        return "Unassigned (matched the search; no abstract to tell which project)"
    return f"{conf[key]['name']} (`{key}`, {conf[key]['page']})"


def post_body(new_by_project, pending, conf):
    order = [k for k in list(conf) + [UNASSIGNED] if k in new_by_project or k in pending]
    n_new = len({frozenset(c["ids"]) for cs in new_by_project.values() for c in cs})
    lines = [f"@sfseiji {n_new} new candidate paper(s) for the project pages. Nothing has been added yet.", "",
             "To approve a paper, add its id under `papers` in `data/projects.yaml`; to dismiss it, "
             "add it under `exclude`. Approved papers appear after the next weekly run (or run the "
             "\"Update publications\" workflow by hand). Undecided candidates are listed again for "
             f"{PENDING_DAYS} days.", ""]
    for key in order:
        if key in new_by_project:
            lines.append(f"### {section_title(key, conf)}")
            lines += [cand_line(c) for c in new_by_project[key]]
            lines.append("")
    if any(pending.values()):
        lines.append("### Still waiting for a decision")
        for key in order:
            name = conf[key]["name"] if key in conf else "Unassigned"
            for c in pending.get(key, []):
                ref = (f"[arXiv:{c['id']}](https://arxiv.org/abs/{c['id']})"
                       if re.fullmatch(fnp.ARXIV_NEW, c["id"]) else md(c["id"]))
                lines.append(f"- {md(name)}: {ref} {md(c.get('title'))} (first listed {c.get('date')})")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
def main():
    cfg = yaml.safe_load(PROJECTS_YAML.read_text())
    conf, det = cfg["projects"], cfg.get("detect") or {}
    failed = [f"projects.yaml {e}" for e in validate(conf)]
    for f in failed:
        print(f"::error::{f}")
    pubs = json.loads(PUB_JSON.read_text())["papers"]
    pubs_by_id = pub_index(pubs)
    state = json.loads(STATE_JSON.read_text()) if STATE_JSON.exists() else {}
    cached = {m["key"]: m for ms in (state.get("projects") or {}).values() for m in ms}
    reported = {k: dict(v) for k, v in (state.get("reported") or {}).items()}
    today = datetime.date.today().isoformat()

    # 1-2) approved lists -> pages
    items = [it for c in conf.values() for it in c.get("papers") or []]
    try:
        found = openalex_lookup(items, pubs_by_id)
    except Exception as err:
        print(f"::warning::OpenAlex metadata lookup failed: {type(err).__name__}: {err}")
        failed.append("metadata lookup")
        found = {}

    projects_out = {}
    for key, c in conf.items():
        entries = []
        for it in c.get("papers") or []:
            k = item_key(it)
            m = meta_for(it, find_pub(it, pubs_by_id, found.get(k)), found.get(k), cached.get(k))
            if m is None:
                print(f"::warning::{key}: no metadata for {k} yet; left off the page this week")
                failed.append(f"{key}:{k}")
                continue
            entries.append(m)
        entries.sort(key=sort_key, reverse=True)
        projects_out[key] = entries
        try:
            if rewrite_page(ROOT / c["page"], key, entries):
                print(f"{c['page']}: list updated ({len(entries)} papers)")
        except (OSError, ValueError) as err:
            print(f"::error::{key}: {err}")
            failed.append(f"{key} page")

    # 3) candidates
    raw = {}
    if det.get("search"):
        try:
            for k, cs in search_candidates(conf, det).items():
                raw.setdefault(k, []).extend(cs)
        except Exception as err:
            print(f"::warning::OpenAlex title/abstract search failed: {type(err).__name__}: {err}")
            failed.append("search")
    for key, c in conf.items():
        d = c.get("detect") or {}
        if d.get("fulltext"):
            try:
                raw.setdefault(key, []).extend(fulltext_candidates(d["fulltext"], det.get("fulltext_days", 90)))
            except Exception as err:
                print(f"::warning::{key}: OpenAlex full-text search failed: {type(err).__name__}: {err}")
                failed.append(f"{key} full-text search")
        for feed in d.get("feeds") or []:
            try:
                raw.setdefault(key, []).extend(feed_candidates(feed))
            except Exception as err:
                print(f"::warning::{key}: feed {feed['url']} failed: {type(err).__name__}: {err}")
                failed.append(f"{key} feed")

    decided_by = {}
    for key, c in conf.items():
        ids = set()
        for it in (c.get("papers") or []) + (c.get("exclude") or []):
            ids |= set(item_ids(it)) - {None}
        decided_by[key] = ids
    decided = set().union(*decided_by.values()) if decided_by else set()
    reported_ids = {k: {i for v in r.values() for i in v.get("ids", [])} for k, r in reported.items()}

    new_by_project, total = {}, 0
    for key in list(conf) + [UNASSIGNED]:
        if key not in raw:
            continue
        if key == UNASSIGNED:
            skip = decided | set().union(*reported_ids.values()) if reported_ids else set(decided)
            titles = {fnp.title_norm(m["title"]) for ms in projects_out.values() for m in ms}
        else:
            skip = decided_by[key] | reported_ids.get(key, set())
            titles = {fnp.title_norm(m["title"]) for m in projects_out[key]}
        merged = []
        for cnd in raw[key]:
            ids = cand_ids(cnd, pubs_by_id)
            if ids & skip or fnp.title_norm(cnd["title"]) in titles:
                continue
            same = next((m for m in merged if m["ids"] & ids), None)
            if same:
                same["ids"] |= ids
                if cnd["why"] not in same["why"]:
                    same["why"].append(cnd["why"])
                continue
            merged.append(dict(cnd, ids=ids, why=[cnd["why"]]))
        merged.sort(key=lambda c: c.get("date") or "", reverse=True)
        room = MAX_REPORT - total
        if merged and room > 0:
            new_by_project[key] = merged[:room]
            total += len(new_by_project[key])
        if len(merged) > max(room, 0):
            print(f"::notice::{len(merged) - max(room, 0)} candidate(s) for {key} held for next week (post size cap)")

    pending = {}
    cutoff = (datetime.date.today() - datetime.timedelta(days=PENDING_DAYS)).isoformat()
    for key, r in reported.items():
        for pid, v in sorted(r.items(), key=lambda kv: kv[1].get("date", ""), reverse=True):
            if v.get("date", "") >= cutoff and not set(v.get("ids", [])) & decided:
                pending.setdefault(key, []).append(dict(v, id=pid))

    if new_by_project:
        try:
            url = post_candidates(post_body(new_by_project, pending, conf))
            if url:
                print(f"Posted {total} candidate(s): {url}")
                for key, cands in new_by_project.items():
                    r = reported.setdefault(key, {})
                    for cnd in cands:
                        pid = cnd.get("arxiv") or cnd.get("doi") or cnd.get("bibcode")
                        r[pid] = {"date": today, "title": cnd["title"], "ids": sorted(cnd["ids"])}
            else:
                print(f"{total} candidate(s) found but not recorded as reported (nothing posted)")
        except (urllib.error.URLError, OSError, ValueError) as err:
            # not recorded as reported, so next week tries again
            print(f"::warning::could not post the candidates: {type(err).__name__}: {err}")
            failed.append("issue")
    else:
        print("No new candidates.")

    new_state = {"projects": projects_out, "reported": reported}
    if new_state != {k: v for k, v in state.items() if k != "updated"}:
        new_state["updated"] = today
        tmp = STATE_JSON.with_name(STATE_JSON.name + ".tmp")
        tmp.write_text(json.dumps(new_state, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(tmp, STATE_JSON)

    if failed:
        print(f"::error::{len(failed)} step(s) failed: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
