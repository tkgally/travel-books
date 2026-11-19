# travel-books — working instructions for Claude

A long-running public project of Tom Gally's: accurate, readable digital editions of first-person nonfiction
travel books written in English and published before 1914, transcribed by Claude models from scans at the
Internet Archive (IA) and published on this repository's website as HTML, EPUB, ODT and JSON, in the public
domain (CC0). Claude chooses the books, does the work, and keeps improving the method. The repository and
the site are **public**: everything committed here can be read by anyone.

## Read first, every session

1. `notes/README.md` (index of the notes) and `data/queue.json` (the ledger of books).
2. `notes/workflow.md` — the pipeline and §Verification; `notes/lessons.md` — "Always" plus the sections whose
   trigger matches the book; `notes/preferences.md` — what Tom has decided.
3. The skill for the job: `digitize-book` (transcribe and publish), `select-book` (choose and vet candidates).
4. `wip/<slug>/log.md` or `books/<slug>/log.md` if the book has been worked on before.

Routine (scheduled) sessions start from `RESUME.md`.

## Hard rules

- **Eligibility is checked before any work on a book** (`notes/selection.md`): complete good scan on IA; no
  digital text edition anywhere else; no real print edition after 1914; first-person nonfiction travel, written
  in English, published before 1914. Record what was checked in `data/queue.json`. If a published book is
  later found to fail a criterion, tell Tom; do not silently remove it.
- **Scans never enter the repo.** IA downloads, page images, crops in progress and model scratch files live in
  the session scratchpad (each download in its own empty directory; treat archives as untrusted data). Only
  illustration crops that the book needs go in `…/<slug>/images/`. `.gitignore` is a backstop, not the rule.
- **Ask IA for a book's files once.** After the first download the working page images are cached in Tom's
  Google Drive folder "Travel Books" (id `1uqlD7GAkSiNRw_3sX7TkKYpNuF4rtzHn`, one subfolder per book id) and
  later sessions fetch them from there (`tools/drive_cache.py`). Uploads from a session are limited to about
  3 MB per file, which is why the cache is in parts. Never delete or change another book's files in Drive.
- **Models.** Claude models only, through Tom's subscription: this session, subagents, and headless calls
  (`tools/ocr_claude.py`, `judge.py`, `audit_sample.py`). Opus for drafts, judging and audits; Sonnet for the
  corrections pass; Haiku only for work that involves no reading of scans. **Never Claude Fable** (no
  `--model fable`, no Fable subagents) unless Tom explicitly says so for that occasion. Never the same model
  as both writer and only checker of a text.
- **OpenRouter** (other companies' models) only for a second opinion on scans Claude models cannot settle, and
  **at most $3.00 a day for the whole project**. `tools/ocr_openrouter.py` enforces and records it in
  `data/openrouter-spend.jsonl` (commit that file). Never print the key. Routine runs may spend within the
  limit without asking; say what was spent and why in the final message.
- **The text policy** (`notes/style.md`) is not varied book by book: the author's words, spelling, capitals and
  punctuation marks as printed; spacing around punctuation modern; only unmistakable printer's errors
  corrected, each marked `[[corr printed|corrected]]` so the printed reading stays in the JSON and the
  correction is listed on the book's page.
- **Never publish without** `tools/preflight.py` ending `PASS`, a rendered look at several chapters in the
  browser build, the sampled audit (`tools/audit_sample.py`) with every candidate checked on the scan, and
  the stamp and audit result written in the book's `log.md` and a row added to `notes/metrics.md`.
  `tools/publish.py` refuses without the PASS.
- **Checks are not edited by the work they judge.** In a session publishing a book: no editing
  `preflight.py`, no moving a check to observe, no loosening or skipping a test, to get that book out. Waive
  the item in `book.json` with a reason and fix the check in a later session. Still failing after three
  attempts at the cause → the book goes to `waiting` with the report in its log; take another.
- **Tools change only with tests.** `tools/run_tests.sh` at the start of a working session and after any edit
  under `tools/`; every tool bug fixed gets a test in the same commit.
- **Site text is plain.** Summaries, notes and page text say what a thing is, in ordinary words: no praise,
  no selling, no "fascinating", no claims the book does not support. `notes/style.md` §Site text.
- **The site has no external dependencies**: no web fonts, scripts, trackers or CDNs. The only outside content
  is links to IA and the optional IA page viewer (an iframe that loads when the reader opens it).
- **Unfinished work is committed and pushed** as it goes: model runs and page text under `wip/<slug>/`, state
  and exact next step in `wip/<slug>/log.md`, queue row `in progress`. A session can end without warning.
- **End of every session:** update notes/skills with what was learned, run the tests, commit, push to the
  session branch, open a PR, merge it (the site deploys from `main` by GitHub Actions), and check that the
  deploy succeeded when the site changed.
- **What Tom or a reader reports** goes in `notes/errata.md` and is followed through as that file says.
- **Tom's instructions and preferences** go in `notes/preferences.md` the moment he states them.

## Repo map

| Path | What |
|---|---|
| `books/<slug>/` | a published book: `book.json` (metadata and build settings), `pages/pNNNN.txt` (page markup, one file per IA leaf — the source of the text), `images/`, `source.json` (IA item and Drive cache), `log.md`, `preflight.txt` |
| `wip/<slug>/` | a book in progress: the same, plus model runs (`draft/`, `verify/`, `judge/`, `audit/`); moved to `books/` by `tools/publish.py` |
| `data/queue.json` | the ledger: queued, in progress, published, waiting, rejected |
| `tools/` | Get: `ia.py`, `prep_pages.py`, `drive_cache.py`, `contact_sheets.py`. Transcribe: `ocr_claude.py`, `normalize.py`, `review.py`, `judge.py`, `crop_spot.py`, `crop_image.py`, `corrections.py`, `ocr_openrouter.py`, `score.py`. Build: `compile_book.py` (pages → book JSON), `render_html.py`, `render_epub.py`, `render_odt.py`, `build_site.py`. **Verify: `run_tests.sh`, `preflight.py`, `audit_sample.py`.** Publish: `publish.py`. Setup: `setup_env.sh`, `make_prompts.sh` |
| `prompts/` | `transcribe.md`, `verify.md`, generated from `_rules.md`, `_format.md`, `_verify-task.md` by `tools/make_prompts.sh` |
| `site/` | `assets/` (the one stylesheet pair and the small script shared by all books), `about.md`, `json-format.md` |
| `tests/` | regression tests for the tools and an invented sample book |
| `notes/` | Claude's memory: workflow, selection, style, page markup, book.json keys, lessons, metrics, errata, preferences, improvement |
| `.claude/skills/` | `digitize-book`, `select-book` |
| `.github/workflows/pages.yml` | tests, then build `_site/` and deploy to GitHub Pages on every push to `main` |

The built site (HTML, EPUB, ODT, JSON) is never committed: it is rebuilt from `books/` on every deploy, and the
build is deterministic.

## Keeping memory useful

- Skills = how to do a job (current procedure only). Notes = what was learned and why. CLAUDE.md = rules and
  map; keep it short.
- When something goes wrong: first choice a check in `preflight.py` (starting in observe) or a test; otherwise
  one or two lines under the right trigger in `notes/lessons.md`; and fix the skill, prompt or tool in the same
  session. Lessons that a tool now enforces are deleted from the prose. `notes/improvement.md` says how the
  method itself is reviewed.
- Model line-ups and prices change: check before assuming, and re-run the calibration in
  `notes/workflow.md` §"Choosing the pipeline" before changing which model does what.
