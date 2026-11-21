# A Parson’s Holiday — W. Osborn B. Allen (1885)

IA: parsonsholidaybe00alle (University of California Libraries, Los Angeles; 252 leaves, 400 ppi, colour).
Eligibility: queued 2026-11-21 after vetting by an Opus subagent; re-checked by the session the same day: not in
pg_catalog.csv; no free text or reprint found; author born 1849 (Allen of Bicton genealogy), death not found, so rule 5
by the birth year (Tom 2026-11-19). The map is by W. Hughes (William Hughes, 1818–1876), published by George Philip & Son.

## Status
Published v1 2026-11-21.

## Page map
p0000 cover (hidden; plain black cloth) · p0001 spine · p0002–p0005 bookplate, endpapers, blanks · p0006 folding map
"India and Ceylon" (W. Hughes; George Philip & Son), fully opened · p0007 title (i; offset 6) · p0008 blank ·
p0009 dedication (iii) · p0010 blank · p0011–p0012 preface (v–vi, April 1885) · p0013–p0014 contents (vii–viii) ·
p0015 = p. 1 (offset 14; head title) … p0239 = p. 225 "FINIS." · p0240–p0242 index (pp. 226–228; printer's imprint) ·
p0243–p0251 endpapers, covers, colour card (p0247–p0251 hidden). No half-title, no list of illustrations.
Footnotes (from the sheets): p0057, 0067, 0068, 0081, 0090, 0095, 0106, 0109, 0127, 0129, 0132, 0136, 0165, 0166, 0178,
0183, 0206, 0212, 0228–0231. Verse: p0037, p0084–p0085 (Tennyson), p0174–p0176 (a long poem, probably Lyall).
Scan check: all sheets, 23 folios at full size (Opus subagent), 2026-11-21: GOOD. Cover: the title page (cloth plain).

## Decisions
- p0176 (p. 162) refused by the output filter in the draft: `ocr_fallback.py` (tesseract + Opus correction), then the
  Sonnet pass and the judge as usual; spot-read word for word (right) and audited alone (5/5); said in notes_on_text.
- No "Chapter I." is printed: p0015 has only the head title "A Parson’s Holiday." as its heading; book.json gives that
  division the title "Chapter I" (pager, breadcrumb) while the page shows the printed heading.
- Contents: each chapter's entry is "Chapter N." and its printed summary (`toc_title`); the printed contents p0014 was
  drafted as centred lines and made a table like p0013. The folding map is the `frontispiece` (first reading division).
- Printer's errors marked: p0082 annnexation, p0129 alway, p0176 "he he", p0229 hadly. Kept as printed: Portugese
  (p0075, p0166), meretorious (p0136).
- Spot-read overturned the judge once: p0064 Pathán (acute; the judge kept the draft's Pathân). p0177 viá (acute on a).
- Accents as printed: Brahman/Bráhman, Dewan/Dewân, ghàt/ghât, Mahal/Mahál, Nirvana/Nirvâna, Peshwa/Peshwá,
  Rajput/Rájput, Tipu/Tipú.
- keep_hyphens: p0033 (ear-rings), p0212 (self-denial).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-21 | opus | 237 (p0006–p0242) | 15.99 | 1 refused (p0176) → fallback ($0.07) |
| corrections | 2026-11-21 | sonnet | 237 | 7.82 | 4 changes |
| judge | 2026-11-21 | opus | 3 spots | 0.12 | overturned once on the scan (Pathán) |
| audit | 2026-11-21 | opus | 6 + p0176 | 0.41 | 30/30 and 5/5; 0 candidates |
| scan check, spot-read (~40 pages), rendered look | 2026-11-21 | Opus subagents | – | – | 4 misprints, 2 accents |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-21 | PASS, 0 waived; look: hyphen-joins 7, joins 1 (dedication), contents 11 (summaries in toc_title), verse-joins 1 (one stanza, checked), accents 10 (as printed) — tools@ae7a41bc | 30/30 + 5/5; 0 real | Claude $24.34 |

## Known issues
