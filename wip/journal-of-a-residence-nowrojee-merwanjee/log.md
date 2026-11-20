# Journal of a Residence of Two Years and a Half in Great Britain — Jehangeer Nowrojee and Hirjeebhoy Merwanjee (1841)

IA: journalofresiden00jaha (Getty Research Institute; 538 leaves; 600 ppi, crisp). Other scans looked at: none needed.
Eligibility: re-checked 2026-11-20: not in `pg_catalog.csv`; one web search found only catalogue records and
scan-based e-books (Texas A&M, MPDL: page images); first check 2026-11-19 (queue row). Authors' dates not found
(Wadia family, the "Lowjee family" of the Bombay dockyard): both were working assistant builders in 1838 (the
preface: sons/nephew of the master builder Nowrojee Jamsetjee, 1774–1860), so born before about 1818; by
`selection.md` rule 5 (unknown death = died before 100, birth bounded by career) dead before 1918. The
frontispiece lithograph: G. Bragg del., J. R. Jobbins litho. (minor illustrators: Tom 2026-11-20, no bar).

## Status
Stage reached: draft done (Opus, 529 pages; p0212 refused by the output filter → `ocr_fallback.py`),
normalized; Sonnet corrections pass running. Page images cached in Drive (41 parts, fetch tested).
Next step: when `verify/` is complete: `normalize.py $W/verify`, `review.py`, `judge.py`, as workflow §3.
Half-finished: —

## Page map
p0000 colour card · p0001 cover (blind-stamped cloth) · p0002 blank · p0003 endpaper with a handwritten
presentation inscription (left out) · p0004–p0005 endpapers with library pencil notes (left out) · p0006
frontispiece (lithograph portrait of Nowrojee Jamsetjee, head builder, Bombay dockyard) · p0007 title ·
p0008 printer's line · p0009–p0010 dedication (to Sir Charles Forbes) · p0011–p0022 preface (printed iv–xvi) ·
p0023–p0030 contents (with chapter summaries) · p0031 = printed 1 (offset 30, constant to p0522 = 492: checked
from IA's scandata and the sheets) · chapters I–XXXV as in the contents (scandata chapter leaves: 31, 56, 60,
65, 69, 94, 106, 123, 128, 131, 141, 173, 180, 194, 216, 225, 246, 262, 276, 318, 330, 337, 342, 347, 349, 354,
372, 388, 392, 395, 415, 481, 495, 509, 517) · p0522 "Finis" and printer · p0523–p0534 publisher's catalogue
(12 pp., "Works relating to India") · p0535 blank · p0536 back cover · p0537 colour card.
Plates: p0006 (frontispiece) only. Tables: p0085, p0090–p0093 (bridges, population, corn), p0289, p0299–p0301
(dockyard), p0307–p0308, p0398–p0399 (newspaper costs), p0479 (tour table). Verse: p0294–p0298, p0312–p0315
(launch songs), p0496–p0508 (albums, epitaphs). Running quotation marks at line starts in long quotations
(p0137, p0167, p0195–p0199, p0264–p0266, p0376–p0383 etc.): `running_quotes.py` after the judge.
Scan check: all 14 sheets looked at 2026-11-20; full size p0006; problems: none (pencil marks in margins p0125).

## Decisions
- Cover image: the title page (the cloth cover is plain blind-stamped).
- Left out of the drafts: p0000–p0005, p0535–p0537 (colour cards, covers, blank and annotated endpapers).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-20 | Opus | 529 (p0006–p0534) | 33.26 | p0212 (printed 182, Westminster Hall) refused by the output filter |
| Fallback | 2026-11-20 | tesseract + Opus | 1 (p0212) | 0.06 | audit it with `--pages p0212` |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
