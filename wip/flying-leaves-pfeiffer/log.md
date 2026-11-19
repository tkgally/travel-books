# Flying Leaves from East and West — Emily Pfeiffer (1885)

IA: flyingleavesfrom00pfeirich (University of California Libraries, Bancroft copy; 322 leaves, 500 ppi, greyscale).
Other scans looked at: none (this one is clean and complete).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv has only Ida Pfeiffer's
books); web searches of the title and of a sentence from p. 73 ("The hotel—in form of an elephant, with an
observatory in the howdah") find no text and no edition. Emily Pfeiffer 1827–1890 (Welsh-born poet).

## Status
**In progress: five pages to take through stage 3, then publish.** The output filter refused the draft of p0116,
p0117, p0118, p0128 and p0129 (Opus twice, Sonnet once; no model will type them). On 2026-11-19 a session not
working on the book ran `tools/ocr_fallback.py` on them: tesseract's reading corrected by Opus, now in
`draft/` (list in `draft/fallback.json`; `draft/_ocr/` is the tesseract text). Nobody has yet looked at those five
drafts. **Do not type or retype these pages in the session** (CLAUDE.md, the output filter).
Everything else for version 1 was done before: draft, Sonnet corrections, Opus judge, scan checks, structure,
front-matter crops, cover, metadata and summary, audit (30/30, 0 candidates) — on the other 300 pages.
Next:
1. `python3 tools/drive_cache.py fetch wip/flying-leaves-pfeiffer/source.json $B/pages`
2. The Sonnet pass on the five into a scratch directory, so that `verify/` and `judge/` of the other pages are not
   touched: copy the five `draft/pNNNN.txt` to `$B/d5`, then `ocr_claude.py --model sonnet --prompt prompts/verify.md
   --images $B/pages --out $B/v5 --corrections --context-text $B/d5 --pages 116-118,128-129`; `normalize.py $B/v5`;
   `review.py $B/d5 $B/v5 --out $B/spots5.json`; `judge.py --spots $B/spots5.json --verified $B/v5 --images $B/pages
   --out $B/j5`; `normalize.py $B/j5`. Copy the `.corr`, verdicts and report into `verify/` and `judge/` under names
   that do not overwrite the earlier ones, and only the five page files into `pages/` (the other files in `pages/`
   have later hand edits).
3. On those five: every Sonnet change and judge spot on a crop; italics (tesseract has none: the correctors added
   them), `[[cont]]` at p0116, p0119, p0128, p0130 (preflight `joins`, `hyphen-joins`), quotation marks.
4. `audit_sample.py --pages p0116,p0117,p0118,p0128,p0129` into `audit-fallback/`; record it in the log.
5. Preflight PASS with `leaves` empty; rendered look at From the West, Leaves III and IV; `publish.py
   flying-leaves-pfeiffer`; versions row, metrics row (say that five pages came by the fallback).

## Page map
p0001 front cover (plain cloth) · p0002 front pastedown, Bancroft Library plate · p0003–p0005 endpapers, blank ·
p0006 IA card · p0007 half-title "Flying Leaves from East and West" · p0008 blank · p0009 title page ·
p0010 verso (library stamps, Leadenhall Press device) · p0011 = printed [1] part half-title "Flying Leaves. From the
East." · p0012 blank · p0013 = printed 3 (offset 10, constant to the end).
From the East — Leaves begin: I p0013, II p0023, III p0038, IV p0049, V p0057, VI p0067; ends p0079 (69).
p0080 blank · p0081 part half-title "Flying Leaves. From the West." · p0082 blank.
From the West — Leaves begin: I p0083 (73), II p0098, III p0114, IV p0126, V p0138, VI p0150, VII p0163,
VIII p0169, IX p0178, X p0190, XI p0199, XII p0215, XIII p0227, XIV p0237, XV p0242, XVI p0255, XVII p0272,
XVIII p0283, XIX p0297; ends p0312 (302, "The End.").
p0313–p0323 endpapers, back cover, colour cards (p0319 not in the archive's numbering).
No contents page, no preface, no index, no advertisements, no plates. Footnotes seen on p0030, p0150, p0171,
p0187. Verse quotations e.g. p0083, p0132, p0181, p0312.
Scan check: all 9 contact sheets looked at 2026-11-19; full size: p0009, p0079–p0083, p0187; problems: none.

## Decisions
- Cover image: the title page (p0009, full size); the cloth cover is plain.
- Structure (assumed): two parts, "Flying Leaves. From the East." and "… From the West." (the printed part
  half-titles, p0011 and p0081), each with its Leaves as chapters (both parts number from Leaf I).
- Chapter openings are a drop capital followed by full-size capitals ("THE bazaars"), so typed as plain capitals;
  the two drafts that had `O<sc>ur</sc>` / `T<sc>wo</sc>` (p0038, p0138) corrected. The 9 corrections-pass
  proposals to `<sc>` openings and 3 on p0010 were rejected by the judge and the scan agrees.
- p0207: printed ‘I guess … long,” (single opening, double closing quotation mark): `[[corr ‘|“]]`.
- p0232 "pistils and stamen": as printed (judge and scan), kept.
- p0133: no `[[cont]]` after the verse at the foot of p0132 (lessons: a sentence resuming after a set-off block).
- The six `[[cont]]` after a full stop (p0025, p0054, p0079, p0130, p0135, p0141): first lines not indented on the
  scan; kept.
- keep_hyphens p0176: "counter-|check" (the author hyphenates counter-appeals, counter-excitements, counter-movement).
- Title-page monogram (p0009-1) and publisher's device (p0010-1) cropped; the IA blind stamp crosses the monogram.
- p0008 (blank) given a page file by hand.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-19 | opus | p0007, p0009–p0312 (305) | 19.04 | 5 refused by the output filter (p0116–p0118, p0128–p0129), each tried 3 times by the tool as it then was |
| Draft retry | 2026-11-19 (later session) | opus | the same 5 | 0.00 | all 5 refused again |
| Fallback draft | 2026-11-19 (diagnosis session) | tesseract + opus corrections | the same 5 | 0.28 | all 5 done; 2–7 corrections each; Sonnet draft of the 5 tried first: refused |
| Corrections | 2026-11-19 | sonnet | 300 | 9.40 | 13 word and 3 markup changes, all applied |
| Judge | 2026-11-19 | opus | 13 spots on 11 pages | 0.50 | sided with the draft 13/13; scan agrees |
| Audit | 2026-11-19 | opus | 6 | 0.34 | 30/30 planted errors found; 0 other differences |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
