# East by West: A Journey in the Recess — Henry W. Lucy (1885)

IA: two volumes, Google scans of Harvard copies (bilevel, 600 ppi): Vol. I eastbywestajour04lucygoog (321 images), Vol. II eastbywest00unkngoog (379 images). JATSI 70.
Eligibility: vetted 2026-11-23 (Opus subagent: rules 1–4 met; print-on-demand only; no Ganesha/Synapse, Elibron or Kegan Paul); re-checked 2026-11-28 (queue row; the only JATSI row now queued that meets every rule).

## Leaf naming (two IA items in one book)
Vol. I IA leaf k = page file `p1000+k`; Vol. II IA leaf k = `p2000+k`. Working images `$B/pages/` built from `v1/pages` and `v2/pages` of `prep_pages.py`, renamed; `leaves.json` there holds both items' data. `source.items` in source.json and book.json.

## Status
Published v1 2026-11-28.

## Page map
Vol. I (printed = leaf − 1012): p1000 Google notice · p1001–p1004 cover, bookplate, endpapers (not drafted) · p1005 half-title · p1006 verso (owner's inscription) · p1007 title · p1008 verso (printer) · p1009 dedication (“To my wife, companion of the journey and co-labourer in its record”) · p1010 blank · p1011 Contents · p1012 blank · p1013–p1315 text pp. 1–303 (“End of Vol. I.”) · p1316–p1320 blanks, endpapers, cover.
Chapters I–XIX: p1013, 1033, 1047, 1062, 1078, 1090, 1104, 1120, 1129, 1145, 1160, 1175, 1194 (XIII, Japan begins), 1215, 1231, 1246, 1268, 1282, 1298.
Vol. II (printed = leaf − 2010): p2000 Google notice · p2001–p2003 (not drafted) · p2004 half-title · p2005–p2006 blanks · p2007 title · p2008 verso · p2009–p2010 Contents · p2011–p2371 text pp. 1–361 (“The End.”) · p2372–p2378 blanks, endpapers, cover.
Chapters I–XXIV: p2011, 2028, 2046, 2067, 2083, 2096 (VI, tables), 2116, 2131, 2151, 2171, 2179, 2197, 2210, 2229, 2250, 2260, 2273, 2290, 2302, 2317, 2330, 2338, 2346, 2356.
No illustrations, no index. Ornaments: the publisher's device on the title pages only.
Scan check: all 18 sheets, 22 leaves at full size (Opus subagent, 2026-11-28): good; page numbers followed through both volumes.
Notes: running heads; signature marks (“VOL. I. 19”) to drop; statistical tables Vol. II ch. VI (p2100–p2114, wide ruled tables); verse p1192–p1193, p1311, p2131, p2158, p2175 (French, Hugo), p2351, blackletter couplet p2371; a letter misspelt on purpose p1301; romanized Japanese with accents and circumflexes (Jôruri).

## Decisions
- Two volumes as one book (as *Embassy to China*): `source.items`; parts “Volume I” (p1013, the printed head “East by West.” above Chapter I) and “Volume II” (p2011); Volume II's half-title (p2005, kind `front`) and title page (p2007, `titlepage`, “Title page of Volume II”) as in *Embassy*. Each volume's chapters numbered from I as printed (`notes_on_text`).
- The verse on p1006 and p2006 (“We had thought at least, with the wind in the East …”) is a handwritten owner's inscription, not print: the leaves are typed blank (the scan check had called them inscriptions; the draft typed the verse).
- Cover: plain cloth (Google scan): `cover.jpg` is the title page of Volume I. The publisher's device on both title pages cropped as ornaments.
- Printer's errors marked: stateman, practially, tbe, superflous, appearace, a missing stop (p1107), qu’ou (Hugo). Left as printed: crounching, da cappo, dilemna (possibly the author's), frighted, awaked.
- Vol. II ch. VI tables checked cell by cell and summed: three printed totals do not add up (revenue, area, births 1877); the cells match the scan, so the book's figures stand.
- The letter p1301 (misspelt on purpose) is in body type: plain paragraphs. `keep_hyphens` p1159 (gambling-house), p2021 (dining-room).
- Contents: printed chapter titles (short); no editor's entries needed.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-28 | preflight PASS: east-by-west-lucy v1 — 0 to fix, 0 waived; to look at: hyphen-joins 8, folios 1, accents 10, rare-forms 4, serial-commas 2, missing-stop 3 — tools@96e14a45 2026-11-28 | 30/30; 0 real errors / 6 pages | rendered look (Opus subagent, all 49 pages at 390 px, key pages at 1280): the Vol. I imprint set in small capitals as printed, with “G. C. & C.” |
| Draft | 2026-11-28 | Opus | 679 | 45.08 | no refusals, no 〓 |
| Corrections | 2026-11-28 | Sonnet | 679 | 22.72 | 17 changes; 2 not applied (both right as drafted); a `[[cont]]` proposal p2327 (wrong) |
| Judge | 2026-11-28 | Opus | 16 spots | 0.62 | draft 12, verified 4 |
| Spot-read | 2026-11-28 | Opus subagent | front matter, chapter openings, tables (sums), verse, letter, lists, tess_compare | — | 8 printer's errors marked, a dêbris accent, ditto marks „, 2 `[[cont]]`, letter unwrapped |
| Audit | 2026-11-28 | Opus | 6 | 0.34 | 30/30; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
- The part pages “Volume I” and “Volume II” show only the printed head “East by West.” (as in *Embassy to China*).
- The dedication's date line is printed flush left; the markup has no flush-left paragraph, so it shows indented.
- Wide tables in Vol. II ch. VI scroll inside their box on narrow screens; group headings have no column spans.
