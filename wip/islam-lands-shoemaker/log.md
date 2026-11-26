# Islam Lands — Michael Myers Shoemaker (1910)

IA: islamlandsnubias00michrich (University of California Libraries; 378 leaves, 500 ppi). Other scans:
39020001791345-islamlandsnubia (George Washington University, 300 ppi; the same edition).
Eligibility: queue row (Opus subagent, re-vetted 2026-11-26: no text elsewhere, no reprint). Re-checked 2026-11-26 (IA
search: the two scans only). Started 2026-11-26.

## Status
Stage (a) done: scan checked (Opus subagent), cached in Drive (23 parts). The plate “The Temple of Jupiter at Dougga” (facing
p. 142) is missing from the UC copy: taken from the GWU copy (n228) as p0231a. Stages to audit done, preflight PASS; rendered look, then publish.

## Page map
Scan check (Opus subagent, 2026-11-26): text complete (i–xii, 1–251); one plate missing (above). No p0000; files p0001–p0379,
no p0375. p0001 cover (plain cloth, no title: the title page is the picture) · p0002–p0007, p0009 endpapers, blanks · p0008
“By the same author” · p0010 frontispiece (tissue guard p0011–p0012, not drafted) · p0013 title page · p0014 imprint · p0015
dedication · p0016 blank · p0017–p0018 Preface iii–iv · p0019–p0022 Contents v–viii · p0023–p0026 Illustrations ix–xii ·
p0027 half-title “Islam Lands” · chapters (leaf/page): I 29/1 · II 55/19 · III 77/33 · IV 95/45 · V 139/75 · VI 175/99 ·
VII 189/109 · VIII 214/128 · IX 237/147 · X 252/158 · XI 281/179 · XII 295/192 · XIII 322/214 · XIV 336/226 · XV 351/239 ·
end p0360 (p. 248) · p0361–p0363 Index · p0364 blank · p0365–p0367 Putnam's advertisements · p0368–p0379 blanks, slip,
endpapers, back cover, colour charts. Plates (each with a blank verso), many sideways: p0010, 33, 39, 45, 51, 57, 63, 69, 75,
81, 87, 93, 99, 105, 111, 117, 123 (plan of the Palace at Khartoum), 129, 135, 141, 147, 153, 159, 165, 171, 177, 185, 193,
201, 209, 217, 225, 231a, 239, 247, 255, 263, 271, 279, 287, 299, 313, 325, 337. Chapter synopses in small type; footnotes;
short verse; letters and telegrams (Gordon chapters).

## Decisions
- Divisions: “By the same author” (front), title page (frontispiece moved to it), dedication, preface, contents and list of
  illustrations (JSON only), half-title and the book's title above Chapter I (front), 15 chapters, index (JSON only),
  Putnam's advertisements. p0009 a blank page file; p0011–p0012 (tissue guard) waived in `leaves`.
- Contents: the chapters have no titles, only long summaries (`[[subtitle]]`); entries of the editor's naming the places,
  from the summaries (said in `notes_on_text`).
- Captions: the plates' credit lines (“From a photograph by …”, typed by the draft as `[[right]]` lines or second
  captions) joined into the one `[[caption]]` after the caption and a full stop, as in *An Autumn Tour in Western Persia*;
  no full stop added at the end. The stray second captions crashed the compiler (fixed, test `StrayCaptionThenCont`).
- Corrections pass: 32 changes, 23 spots judged: 14 draft, 8 verified; the verifier's small capitals for chapter openings
  rejected (the print has a drop capital and the rest of the word in full capitals); p0259 `[[cont]]` added by the verifier
  wrong (indented); p0360 closing “Islam Lands.” restored from the draft.
- Spot-read (Opus subagent; quotations measured by line spacing, body 45 px, small type 42 px): p0080, p0169–p0170, the
  first paragraphs of p0173 and p0179 put in `<blockquote>`; title page split as printed; printed misprints marked p0021
  “Egyptains”, “Gity” (contents), p0296 “enthusiam”, p0312 “cirumstance”, p0342 “somethin”. tess_compare's pitch test
  missed these pages (ratio 0.93): its threshold 0.88 is for type a size smaller.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-26 | opus | 359 | 22.90 | no refusals, no 〓 |
| corrections | 2026-11-26 | sonnet | 358 | 11.47 | 32 changes |
| judge | 2026-11-26 | opus | 23 spots | 0.96 | 14 draft, 8 verified |
| audit | 2026-11-26 | opus | 6 | 0.33 | 30/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
