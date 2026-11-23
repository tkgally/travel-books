# A British Officer in the Balkans — Percy E. Henderson (1909)

IA: britishofficerin00hend (University of California; 402 leaves, 400 ppi). Other scan: britishofficerin00henduoft (Toronto, Lippincott issue).
Eligibility: re-checked 2026-11-23: web search finds no English text or reprint (PG #27659 is a Dutch translation). Henderson born 1852 (LC); death date not found (birth-before-1856 rule). Photographs the party's own.

## Status
Stage reached: (a) Tom said on 2026-11-23 to publish it with the photographs (preferences.md); in progress again, to be published next session.
The scan check found it only after the Opus draft had been started (the session started the draft before the check came back: a mistake; lesson written). Draft stopped at 382 of 398 leaves ($27.60); `ocr_claude.py` resumes: the same command finishes the rest.
Next step: finish the draft (`--pages 2-395`, then delete drafts of p0013–p0014, the 1989 bindery notice, and of hidden leaves), then workflow §3.

## Page map
p0001 cover · p0002–p0006 endpapers, blanks · p0007 half-title · p0009 frontispiece “A Bosnian Beauty” (verso p0010 blank) · p0011 title (“With 50 Illustrations & a Map”) · p0012 imprint · p0013–p0014 U.C. bindery notice of 1989 (replacement photocopy volume; not part of the book) · p0015–p0020 contents (5–10) · p0021–p0022 list of illustrations (11–12; credit to Mrs. Henderson) · p0023 Part I (13) · p0025 = printed 15, Ch. I (offset +10, +2 after each plate) · Part II p0087 (63) · Part III p0181 (139) · Part IV p0215 (163) · p0367–p0374 index (295–302) · p0375–p0392 Seeley advertisements · p0393–p0400 blanks, back cover.
Chapters (leaf/page): I 0025/15 · II 0035/23 · III 0047/31 · IV 0067/45 · V 0089/65 · VI 0107/79 · VII 0116/88 · VIII 0129/99 · IX 0150/114 · X 0163/123 · XI 0170/130 · XII 0183/141 · XIII 0202/152 · XIV 0211/159 · XV 0217/165 · XVI 0226/174 · XVII 0247/191 · XVIII 0259/201 · XIX 0271/209 · XX 0279/217 · XXI 0296/230 · XXII 0315/247 · XXIII 0325/257 · XXIV 0335/265 · XXV 0347/275 · XXVI 0358/286.
Plates (blank versos): p0027, 39, 43, 49, 55, 63, 83, 93, 99, 123, 131, 137, 141, 151, 157, 177, 185, 189, 193, 197, 207, 231, 241, 249, 261, 267, 283, 293, 311, 327, 339 (sideways: 39, 43, 185, 189, 193, 293, 327); 50 photographs with the frontispiece. The map is missing from this copy (and not seen in the Toronto copy).
Scan check: all 11 sheets and 12 leaves at full size by an Opus subagent 2026-11-23: text complete (pp. 5–302), sharp; the copy is a 1989 photocopy replacement volume, plates muddy but captions readable. Drive cache: 25 parts.

## Decisions
- 2026-11-23: the book's title repeated above Chapter I (p0025) left out, as a head-title (the verifier and the judge agreed). Running heads typed as headings by the draft removed (p0026, p0037, the contents and index continuation pages; p0120 and p0342 left out by the judge, checked on the scan).
- Captions: the printed title and the descriptive line of each plate are one `[[caption]]` line, as in the other books (the compiler joins them; preflight compares caption lines one by one).
- First words of chapters (a drop capital and the rest of the word in capitals) typed in capitals: “THE island”, “AN interesting”.
- p0080 “Nieguš”, p0134 “ferediza” (a Cyrillic letter in the draft) settled on the scan.
- The full-size plate leaves were not extracted when the scan was first fetched; the jp2 archive was fetched from IA a second time on 2026-11-23 for them.
- Photographs cropped in grey (`--gray`) from the photocopy; cover.jpg = the title page (the cloth cover has no title).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-22/23 | Opus | 394 | 28.65 | stopped at 382 for the eligibility question; finished 2026-11-23 ($1.05) |
| corrections | 2026-11-23 | Sonnet | 392 | 13.67 | 22 spots |
| judge | 2026-11-23 | Opus | 22 spots | 0.98 | draft 12, verified 5, neither 3, could not undo 2 (running heads) |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
