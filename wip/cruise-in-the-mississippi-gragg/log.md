# A Cruise in the U.S. Steam Frigate Mississippi — William F. Gragg (1860)

IA: cruiseinussteamf00grag (Library of Congress; 82 images, 400 ppi). JATSI 14.
Eligibility: queued 2026-11-20 (Opus subagent); re-checked at the start the same day (not in pg_catalog.csv; a web
search of the title finds only the IA scans). Author 1810–1864 (Bedford Historical Society). Taken up 2026-11-20.

## Status
Stages (a)–(c) done; preflight PASS, audit 30/30; rendered look next, then publish.

## Page map
Scan check 2026-11-20 (the session: all 3 contact sheets; full size p0078): PASS except the last leaf.
p0000 cover outside (dark) · p0001 front wrapper (printed: title within a rule border) · p0002 inside of wrapper, blank ·
p0003 title page · p0004 dedication "Respectfully Dedicated to Dr. Philip S. Wales, U.S.N. by the Author" (LoC stamp) ·
p0005 Prefatory Note · p0006 blank · p0007 = p. 5 "Cruise of the Mississippi." (text starts) … p0077 = p. 75 ·
p0078 = p. 76, last page: **cut at the right edge** (one to three letters a line lost) and a LoC barcode label above
the text → replaced by **p0078a** = UC copy acruiseinusstea01graggoog page n80 (bilevel, 600 ppi, complete), made
1800 px high grey; p0078 itself is not transcribed (preflight `leaves` counts p0078a for it; no waiver needed). · p0079 back wrapper · p0080–p0081 IA colour
cards · p0082–p0083 blank.
Printed-page offset: leaf − 2 throughout (p0007 = p. 5). No chapters, no contents, no illustrations, no index.
A running narrative in paragraphs; lists of officers (p0007) and of the deaths and distances may come up in the text.

## Decisions
- Draft with `--halves` (small type on a large page; 76 pages, so the extra cost is small).
- Judge: 3 spots. p0007 "dismised" and p0064 "Mississipi’s": printed so (crops) → `[[corr]]`. p0060 "hȧd": a speck → "had".
- p0007: "Stemb'e" is a broken *l* (the book prints "Stemble" later; the UC copy has the same break) → "Stemble", no corr.
  "G. 〓. Bacon": the initial is under a blot in the LoC copy; the UC copy (n9) reads "G. N. Bacon". Said in notes_on_text.
- Blank leaves p0002, p0006 given `[[blank]]` page files. keep_hyphens p0008 ("forty-five").
- Contents: no chapters, one division of 72 pages → 11 entries of the editor's (spans of dates and the ports, in the book's
  spellings), proposed by a Sonnet subagent from the draft and checked at paragraph starts. The dedication and the
  Prefatory Note are their own entries. Cover image: the title page (the printed wrapper is cut at the left and labelled).
- Regions added to `data/places.json`: Macau, Madeira, Barbados, United States Virgin Islands.
- Summary: Gragg's place in the crew is not stated in the book (the queue note's "surgeon's steward" is not printed; left out).

## Runs
| Run | Model | Pages | Cost |
|---|---|---|---|
| draft (`--halves`) | Opus | 75 | $8.01 |
| corrections | Sonnet | 75 | $2.58 (3 word changes, 1 markup) |
| judge | Opus | 3 spots | $0.12 |
| audit | Opus | 6 (p0018, p0035, p0039, p0043, p0049, p0056) | $0.37: 30/30, 0 candidates |
Total $11.08.

## Versions

## Known issues
