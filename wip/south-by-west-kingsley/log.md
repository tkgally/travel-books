# South by West; or, Winter in the Rocky Mountains and Spring in Mexico — Rose Georgina Kingsley; ed. Charles Kingsley (1874)

IA: southbywestorwin00king (University of California Libraries; 454 leaves, 400 ppi, greyscale). Other scans
looked at: none (this one is clean and complete).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv; Rose Kingsley's
*Children of Westminster Abbey* and *Roses and Rose Growing* are there, not this); The Online Books Page lists
only page images (a German library); a web search finds only print-on-demand reprints (Kessinger 2007/2010,
Creative Media Partners 2023, others). An ISBN with the Rio Grande Press prefix that came up in the same search
is Schwatka's *In the Land of Cave and Cliff Dwellers* (Open Library), not this book. Rose Georgina Kingsley
1845–1925; Charles Kingsley (editor, preface) 1819–1875. Engravers not named.

## Status
**In progress again (Tom, 2026-11-19: try the refused pages in this book too).** Set aside earlier the same day
after the output filter refused three pages of the Opus draft (p0076, p0109, p0189). There is now a route for such
pages: `tools/ocr_fallback.py` (workflow §2). **Do not type them in the session.**
Stage reached: Opus draft 413 of 432 pages; not normalized. Missing: p0076 p0109 p0189 (refused) and p0424–p0441
(not yet run when stopped).
Next: fetch the pages from Drive (`python3 tools/drive_cache.py fetch wip/south-by-west-kingsley/source.json $B/pages`);
run the draft for the rest (`ocr_claude.py … --pages 424-441`; resumable); `ocr_fallback.py --images $B/pages --draft
wip/south-by-west-kingsley/draft` (it takes the refused pages from the log, including any new ones); `normalize.py`;
then stage 3 as usual, the fallback pages named here and audited. Crops and cover are done (`images/`); the
full-size leaves are not cached, but the crops are final.

## Page map
p0000 colour card (hidden) · p0001 front cover (cloth, agave design stamped) · p0002 front pastedown, UC bookplate ·
p0003–p0004 endpapers · p0005 IA card · p0006 frontispiece "Monument Park" · p0007–p0008 tissue guard (hidden) ·
p0009 title page · p0010 verso (printer) · p0011 dedication "To my Father and Mother" · p0012 blank ·
p0013–p0016 Preface (v–viii?), signed Charles Kingsley · p0017–p0023 Contents · p0024 blank · p0025 List of
Illustrations · p0026–p0028 blank · p0029 = printed 1 (offset 28, constant to the end) Chapter I ·
p0439 = 411 end of text (Chapter XXIV, printer's imprint at foot) · p0440 blank · p0441 advertisement "Works by
Rev. Charles Kingsley" · p0442–p0446 endpapers, library slips, back pastedown · p0447–p0453 back cover, colour
cards, edges.
Chapters begin: I p0029, II p0052, III p0075, IV p0093, V p0105, VI p0115, VII p0126, VIII p0136, IX p0153, X
p0165, XI p0180, XII p0195, XIII p0206, XIV p0212, XV p0235, XVI p0260, XVII p0272, XVIII p0296, XIX p0313,
XX p0337, XXI p0364, XXII p0385, XXIII p0410, XXIV p0427 (from the contact sheets; to be confirmed by headings).
Illustrations (engravings in the text): p0006 (frontispiece), p0057, p0060, p0063, p0065, p0071, p0077, p0079,
p0102, p0103, p0116 (diagram of strata, "Grass." / "Plain."), p0118, p0133, p0142, p0185, p0215, p0226, p0263,
p0320, p0327, p0353. The List of Illustrations has 21 entries; "Monument Creek, 88" still to be matched (p0116
is a diagram; the frontispiece caption reads "Monument Park.—Page 88", so the list's "Monument Creek, 88" probably means this diagram or is a slip — check against the draft's captions).
Tables: p0170 (Raymond's table of Western coals, printed sideways), p0323, p0435 (figures in columns).
Footnotes: several (e.g. p0093, p0211, p0376, p0412–p0413, p0429–p0434).
Scan check: all 12 contact sheets looked at 2026-11-19; full size: p0025, p0116, p0170, p0412; problems: none.

## Decisions
- Drafted p0006 and p0009–p0441; covers, endpapers, IA card and tissue guards left out.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-19 | opus | 413 of 432 | 27.37 | stopped at Tom's request; 3 pages refused by the output filter |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
