# Errata — errors found after publication

Sources: Tom, readers (GitHub issues), later sessions. A report is a claim until it is checked on the scan.

For each item: (1) check it on the scan (`drive_cache.py fetch … --pages`, `crop_spot.py`); (2) if real, fix
the page file and publish a new version (`workflow.md` §"New version"); (3) ask how it got through and add a
preflight check, a test, or a line in `lessons.md` so that it cannot recur; (4) look for the same kind of
error in the other published books; (5) count it in `metrics.md` (last column); (6) answer and close the
issue, plainly. If the report is wrong (the book prints it so), say so and close it.

| Date | Book | Where | Reported | Checked on scan | Fixed in | Follow-through | Status |
|---|---|---|---|---|---|---|---|
| 2026-11-19 | Diary of the Late Rajah of Kolhapoor | contents | Tom: one entry for the whole diary; readers need more, such as spans of dates and places | not a text error | tools and book.json (contents redesign); version 4 by the next session | policy in `preferences.md`, `workflow.md` stage 4 "Contents"; lesson in `lessons.md` "Always"; the other books looked at | open: publish v4 |
| 2026-11-19 | Sketches Awheel in Modern Iberia | contents | Tom: some chapter entries had the places, others only the number | the long summaries were dropped by the compiler (over 80 characters) | `"toc": {"subtitles": "all"}`; version 2 by the next session | as above | open: publish v2 |
| 2026-11-19 | Flying Leaves from East and West | contents | found in the follow-through: the two part titles were taken for chapters, so the Leaves did not nest; and the Leaves had numbers only (Tom: add place names) | not a text error | compiler; test `Contents`; `toc_title` per Leaf; version 2 by the next session | as above | open: publish v2 |
