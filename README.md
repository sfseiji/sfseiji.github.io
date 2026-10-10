# sfseiji.github.io

Personal + group website of Seiji Fujimoto (University of Toronto), served by GitHub Pages.

## Structure

- `index.html`, `pages/*.html` — static pages sharing `includes/header.html` / `includes/footer.html`
  (injected by `site-shell.js`) and the design system in `assets/site.css` ("Cosmic Dawn" dark theme).
- `pages/venus.html`, `grapes.html`, `gnz7q.html`, `glimpsed.html` — legacy-markup subpages
  (still Bootstrap-based); they inherit the theme through `assets/site.css` overrides.
- `data/publications.json` — the publication database rendered by `pages/research.html#publications`
  (filter tabs: Group-led / First author / Student & postdoc led / All) and the
  "Latest results" cards on the home page.

## Publication auto-update (two layers)

1. **Curated (source of truth)** — `publist_auto/` on Seiji's Mac (Dropbox `_claude_code/publist_auto`).
   Triggered when the ADS-library BibTeX export (`input/library.bib`) changes: regenerates the
   Overleaf publication list, the PDF, **and `data/publications.json`**, then commits + pushes here.
   Student/postdoc-led flags come from `publist_auto/students.yaml`.
2. **Weekly scan (this repo)** — `.github/workflows/update-publications.yml` (Saturdays 06:00 UTC)
   runs `scripts/fetch_new_papers.py`: OpenAlex queries (by ORCID and by name, last 180 days) for
   papers with Seiji as author and for member-led (first-author) papers listed in
   `data/group_members.yaml`. Only papers with an arXiv id are added. Anything not yet in the
   database is appended with `"new": true` (shown with a "New" badge). When the paper later enters
   the curated ADS library, the curated entry replaces it; unmatched new entries are carried over.
   The source moved from the arXiv API to OpenAlex on 2026-10-10 because the arXiv API
   rate-limits GitHub runners (HTTP 429). An optional free OpenAlex key can be stored as the
   repository secret `OPENALEX_API_KEY`; without it the anonymous daily budget is used.

To add/remove a group member from the auto-scan, edit `data/group_members.yaml`.
ORCID iDs there were verified against the ORCID registry (2026-07-06).
