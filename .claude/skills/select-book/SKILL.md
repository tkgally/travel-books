---
name: select-book
description: Find and vet candidate travel books for the travel-books project (pre-1914, English, first-person, good Internet Archive scan, no other digital text, not reprinted after 1914) and add them to data/queue.json. Use when the queue is short or Tom asks for candidates.
---

# Select books

Criteria, sources to search and how to choose: `notes/selection.md`. Read it first; this is the procedure.

1. Look at what is published and queued (`data/queue.json`): which regions, periods and kinds of author are
   missing? Search for those. Read the `rejected` list so nothing is checked twice.
2. Find candidates: `tools/ia.py search '<query>'` (subjects such as "description and travel", "voyages and
   travels", a region, a decade; sort by few downloads), bibliographies of travel writing, references in
   books already done. Well-known titles are almost always on Project Gutenberg: look for the lesser-known.
3. For each: `tools/ia.py meta <id>` (page-image archive present? library scan? size?), then the four checks
   of `notes/selection.md`, then **read twenty pages from the middle** of IA's OCR text
   (`https://archive.org/download/<id>/<id>_djvu.txt`). Queue it only if you would want to go on reading.
4. Be polite to servers: about one request a second to any host; no large downloads at this stage.
5. Add the row to `data/queue.json` (`status: queued`): IA identifier, proposed slug, title, author, year,
   place, publisher, images, `checked` date, `eligibility` (what was searched, what was found, what could
   not be checked), `note` (scan quality, plates, anything the transcriber should know). Failures go under
   `rejected` with the reason. A doubtful case (author died after 1955; uncertain reprint) → `waiting` and a
   question in `notes/preferences.md`.
6. Subagents (Opus or Sonnet, never Fable) can vet a list in parallel; give them the criteria and the sources
   in full and ask for what they could not verify. Check a sample of what they return.
