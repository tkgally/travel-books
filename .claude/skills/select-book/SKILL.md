---
name: select-book
description: Find and vet candidate travel books for the travel-books project (pre-1914, English, first-person, good Internet Archive scan, no other digital text, not reprinted after 1914) and add them to data/queue.json. Use when the queue is short or Tom asks for candidates.
---

# Select books

Criteria, sources to search and how to choose: `notes/selection.md`. Read it first; this is the procedure.

0. `python3 tools/ledger.py` shows which queue is short. For more **JATSI** books the candidates are already
   listed: `data/jatsi.json`, in the order of priority and recorded as
   `notes/jatsi.md` says; steps 3–6 below apply to them unchanged, and their rows get `"from": "jatsi"`,
   `"jatsi": <n>`. The rest of this procedure is for the other books.
1. Look at what is published and queued (`data/queue.json`) so that no one kind of author, nationality or
   destination comes to dominate; search widely. Never choose or pass over a book for the author's gender
   (Tom, 2026-11-19: a wide range, no group preferred). Read the `rejected` list so nothing is checked twice.
2. Find candidates: `tools/ia.py search '<query>'` (subjects such as "description and travel", "voyages and
   travels", a region, a decade; sort by few downloads), bibliographies of travel writing, references in
   books already done. Well-known titles are almost always on Project Gutenberg: look for the lesser-known. A text in EEBO-TCP, ECCO-TCP or a
   subscription database does not rule a book out (`selection.md` rule 2, Tom 2026-11-20): early books are open again.
3. For each: `tools/ia.py meta <id>` (page-image archive present? library scan? size?), then the five checks
   of `notes/selection.md`, then **read twenty pages from the middle** of IA's OCR text
   (`https://archive.org/download/<id>/<id>_djvu.txt`). Queue it only if you would want to go on reading.
4. Be polite to servers: about one request a second to any host; no large downloads at this stage.
5. Add the row to `data/queue.json` (`status: queued`): IA identifier, proposed slug, title, author, year,
   place, publisher, images, `checked` date, `eligibility` (what was searched, what was found, what could
   not be checked), `note` (scan quality, plates, anything the transcriber should know). Failures go under
   `rejected` with the reason. An author who died less than 70 years ago → `rejected` with the year the book becomes eligible. Find the death date of **every** author, editor and illustrator whose work is in the book before queuing it, and write it in the row (if it is unknown, the birth year: Tom assumes death before age 100 — `notes/selection.md` rule 5). A doubtful case (uncertain reprint) → `waiting` and a
   question in `notes/preferences.md`.
6. Subagents (Opus or Sonnet, never Fable) can vet a list in parallel; give them the criteria and the sources
   in full and ask for what they could not verify. Check a sample of what they return. They cannot write
   report files (the harness refuses): ask for the report as their reply. Five agents at once got the
   Wikisource API rate-limited for all of them; three at a time, and tell each to fetch `pg_catalog.csv`
   whole (about 21 MB) before trusting a "no match".
7. `python3 tools/ledger.py check` (also in the tests) before committing.
