# A Sportswoman in India — Isabel Savory (1900)

IA: sportswomaninind00savorich (University of California Libraries; 530 image files p0001–p0531, no p0527; 500 ppi colour).
Eligibility: re-checked 2026-11-27: not in pg_catalog.csv (fresh copy; only her *In the Tail of the Peacock*, #28016); web search: the IA text, BHL page images, Blackwell's print-on-demand; no real reprint. Rejected 2026-11-19 only under the old death-date rule, which Tom dropped on 2026-11-26.

## Status
Stage reached: published v1 2026-11-27.

## Page map
p0001 cover (no title) · p0002–p0004 pastedown, bookplates, flyleaf · p0005 half-title · p0007 blank · p0008 frontispiece (photogravure portrait, signed, no caption) · p0009–p0010 tissue (not drafted) · p0011 title · p0012 imprint · p0013 dedication · p0015–p0017 contents · p0019 = printed 1 · p0522 = p. 408 (colophon) · p0523–p0531 blank, slips, back cover, colour cards.
Offset: leaf = page + 18 + 2 × (plates before it).
Each chapter: a divisional leaf (number, title, summary; folio at the foot), a blank, then the opening page with the title again and a verse epigraph. Chapters (divisional/opening): I Pig-Sticking 19/21 · II Peshawur and the Khyber Pass 65/67 · III From Dalhousie into Chamba 113/115 · IV Chamba into Kashmir 159/161 · V Kashmir 203/205 · VI Fourteen Thousand Feet High 247/249 · VII Black Bears 295/297 · VIII Tiger-Shooting 337/339 · IX Snakes.—Delhi 379/381 · X Ootacamund and Anglo-Indian Life 425/427 · XI From an Elephant Kheddar to a Crocodile Tank 461/463 · XII Impressions of Travel 505/507.
Plates (48, blank verso after each; SW = sideways, caption on the right edge reading bottom to top): 27 SW, 35, 41, 49, 55 SW, 71 SW, 87, 91, 97, 107, 119 SW, 123 SW, 137, 145, 151, 163, 179, 183, 189, 197, 217 SW, 223, 233, 237, 243, 253, 259 SW, 267 SW, 273 SW, 287 SW, 299, 305, 309 SW, 317 SW, 345, 355, 365, 373 SW, 395 SW, 409 SW, 415, 421 SW, 429, 437 SW, 455, 465 SW, 477 SW, 509 SW.
Scan check (Opus subagent, 2026-11-27): all 14 sheets; pages 1–408 each found by running head or neighbours; edges and feet clear; a hair over “were” on p0211; running head “Tiger-Shootin” p0367 (printed so). Session looked at p0008, p0011, p0019, p0021. Cover picture: title page p0011.
Notes: verse epigraphs and verse quotations in small type; boxed notices p0265 (a shop card), p0452 (a receipt); Babu English letters in ch. XI; a two-column bill of fare p0499; Hindustani words in italics with accents; no footnotes seen.

## Decisions
- Chapter heads (assumed; easily changed): each chapter's divisional leaf (number, title, summary as `[[subtitle]]`s) is the chapter heading; the number and title repeated on the opening page above the epigraph are left out as a head-title (as in *A British Officer in the Balkans*); said in `notes_on_text`. p0247's summary was typed as body text: made a `[[subtitle]]`.
- Corrections pass (Sonnet, $16.60): 41 changes; no `[[cont]]` proposals, no blank pages filled. Judge (31 spots, $0.94): draft 20, verifier 10, neither 1; 27 looked at on the scan by an Opus subagent: the judge was wrong on p0247 (VI, a speck after the numeral; checked by the session) and p0357–p0358 Godávari (acute, checked by the session); opening capitals, the shop card's comma, small-capital epigraph titles, the Indian-English letters' italic headings all `###`.
- `[[cont]]` removed at p0051, p0052, p0078, p0334, p0445, p0517 (compile: nothing to continue: a verse block before, or a new verse). p0517 continues a sentence after a verse: the markup cannot join it (known issue).
- Spot-reads (two Opus subagents, full tesseract comparison): printed misprints marked: p0240 “tully”, p0501 “witb”, p0490 a full stop for a comma; accents made as printed (Sháh Jehán, Musalmán, Diwán-i-Khás, Sulimán, bárá: acute, not circumflex); p0165 “sycés” → “syces” (a speck; the same word plain on the page; checked by the session); p0161 “tails” in a Kipling quotation kept as printed.
- Rendered look (Opus subagent, 390 and 1280 px): one fault, the paragraph after the shop card joined to it by a wrong `[[cont]]` (p0266, fixed); paragraphs in lower case after verse at p0043, p0109, p0517 are as printed (a sentence resumed after a quotation; the markup starts a new paragraph).
- keep_hyphens: p0271 camping-ground, p0431 gold-dropping.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-27 | opus | 516 | 33.21 | p0199 refused |
| fallback | 2026-11-27 | tesseract + opus | 1 | 0.06 | p0199 |
| corrections | 2026-11-27 | sonnet | 516 | 16.60 | |
| judge | 2026-11-27 | opus | 31 spots | 0.94 | |
| audit | 2026-11-27 | opus | 6 + 1 | 0.37 | 30/30, 0 candidates; p0199 5/5 |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-27 | preflight PASS: sportswoman-in-india-savory v1 — 0 to fix, 2 waived; to look at: hyphen-joins 2, joins 2, quote-balance 1, verse-joins 2, accents 11, rare-forms 8, serial-commas 4 — tools@6a676bfa 2026-11-27 | 30/30, 0 real errors in 6 pages; fallback page 5/5 | First publication. |

## Known issues
- p0517: “but— [verse] the <i>Shannon</i> made her way” — the sentence after the verse starts a new paragraph (the markup cannot continue a paragraph after a block); likewise p0043, p0109.

## Illustrations (crops by an Opus subagent, 2026-11-27; seven looked at by the session)
Frontispiece and 48 plates `--gray`; all 20 sideways plates `--rotate 270`. Captions printed inside the picture's rectangle painted out in paper white before cropping on p0183, p0189, p0223, p0237, p0309 (the pictures untouched). Lettering inside pictures kept (p0223, p0267). cover.jpg = title page p0011.
- Draft (Opus, 516 pages, $33.21): p0199 (printed p. 145, ordinary prose about the hills) refused by the output filter; fallback (tesseract + Opus corrections, $0.06) done. Audit it with `--pages p0199`; say it in `notes_on_text`.
