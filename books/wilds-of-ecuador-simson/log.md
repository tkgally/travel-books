# Travels in the Wilds of Ecuador — Alfred Simson (1886)

IA: travelsinwildsof00sims (University of Toronto; 324 leaves, 650 ppi). Other scans looked at: none yet.
Eligibility: re-checked 2026-11-27: not in a fresh pg_catalog.csv; web search of the title: catalogue records (Wellcome, Quai Branly), the Spectator's review of 1887, print on demand only.

## Status
Stage reached: published v1 2026-11-27.

## Page map
p0000 colour card · p0001 cover · p0002 pastedown (bookplate) · p0003–p0006 blank flyleaves · p0007 title (no half-title) · p0008 imprint · p0009–p0011 contents (lists “Map”; no preface) · p0012–p0013 blank · p0014 folding map (“Ecuador 1877”, Weller; opened, complete) · p0015 = printed 1 (offset 14) … p0284 = 270.
Chapters (leaf/page): I 15/1 · II 34/20 · III 51/37 · IV 63/49 · V 75/61 · VI 89/75 · VII 101/87 · VIII 115/101 · IX 127/113 · X 140/126 · XI 151/137 · XII 165/151 · XIII 178/164 · XIV 196/182 · XV 212/198 · XVI 226/212 · XVII 235/221 · XVIII 250/236 · XIX 264/250. Blank p0211, p0276. Appendices I Záparo vocabulary p0277–p0280, II Piojé words p0281–p0282, III heights p0283–p0284 (colophon). No index. Publisher's catalogue p0285–p0316 (32 pp.). p0317–p0320 blank, p0321 pocket, p0322 back cover, p0323 card.
Scan check (Opus subagent, 2026-11-27): all 9 sheets; folios by tesseract p0016–p0284, the rest by eye; 9 leaves at full size; nothing missing, cut or blurred; a pencil stroke in the margin of p0024. Plates: none but the map; a line of music (bird call) in the text p0098.
Notes: footnotes (some long); tables p0057–p0060 (heights), p0132 (prices), appendix III; a list with a brace p0083; two-column word lists with ditto marks (apps. I–II); four lines of Schiller p0086; Spanish and pidgin Spanish (pp. 227–233); accents (Záparo, Jívaro, Içá).

## Decisions
- Cover: the front cover has no title; `cover.jpg` is the title page.
- Divisions: the map (p0014) is a reading division of its own, “Map”, as the printed contents lists it; the head title above Chapter I is front matter (JSON only); appendices titled from the printed contents; the catalogue (two divisions) is advertisements. Contents: every chapter with its summary in full (`toc.subtitles: all`).
- The list of the expedition's men (pp. 69–70) is a quotation block, one name a line, the brace typed “Ezequiel }” / “Juan } servants,”; the sentence that goes on after it (“and a boy carrying …”) and the one after the Schiller verse (p. 72) are marked `[[cont]]` → `continues` (the new markup of the review after 115 books).
- Tables continued over a page: Appendix II's word list joined with `[[cont]]`; the tables of heights on pp. 43–44 and 269–270 repeat their header in print and stay two tables. The Piojé note on counting is a paragraph between the tables.
- Ditto marks „ as printed; p0314 (catalogue) letters lost at the inner margin supplied, one price a `[[gap]]` (said in `notes_on_text`).
- Period: “1870s” (García Moreno, d. 1875, sanctioned the first journey; no year is given in the book) — assumed.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-27 | PASS, 0 waived (tools@41a47c58) | 29/30; 0 real errors / 6 pages | spot-read (Opus subagent, tesseract): 18 fixes (accents, a printed misprint “specally” marked, p0314 supplied letters, the party list, a run-on after verse); rendered look: tables over pages, the party list, a note in a table. Total model cost $32.63 |
| Draft | 2026-11-27 | Opus | 310 (p0007–p0316) | 21.74 | 0 errors, 0 refused; 〓 only on p0314 (catalogue, inner margin) |
| Corrections | 2026-11-27 | Sonnet | 310 | 10.41 | 16 changes; [[cont]] proposal p0055 wrong; blank p0013 filled with the map (show-through), refused |
| Judge | 2026-11-27 | Opus | 4 spots | 0.13 | draft 3, verifier 1 (Iça, held on the scan) |
| Audit | 2026-11-27 | Opus | 6 | 0.34 | 29/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 2 | 2026-11-28 | preflight PASS: wilds-of-ecuador-simson v2 — 0 to fix, 0 waived; to look at: hyphen-joins 3, folios 1, contents 4, accents 35, rare-forms 5, serial-commas 2 — tools@20d4a8e2 2026-11-28 | text unchanged except listed fixes | review after 125 books, new check `omitted-edges`: the catalogue's first lines stood above its `#` heading and ended the last reading page; heading moved to the page top |


## Known issues
