# An Authentic Account of an Embassy … to the Emperor of China — Sir George Staunton (1797)

IA: `authenticaccount01stau` (vol. I; UC Libraries; 574 leaves, 300 ppi), `authenticaccount02stau` (vol. II; UC
Libraries; 672 leaves), `gri_33125008481562` (folio volume of plates; Getty; 114 images; not yet fetched — its page
images are a 1.2 GB `_images.zip`, not `_jp2.zip`).
Eligibility: an exception by Tom's choice (`notes/preferences.md` 2026-11-19); rule 5 met (Staunton 1737–1801,
Macartney 1737–1806, Gower 1742–1814, William Alexander 1767–1816). The book page and `site/about.md` must say it is
included as an exception (queue note).

## Status
Stage reached (2026-11-20, session 1): tools ready; scan checked; Drive cache complete (99 parts, all with ids;
fetch tested); illustrations cropped (83 files); **Opus draft of vols. I and II done (1,210 pages, 0 errors,
0 refusals)**; draft of the three Getty leaves and the plates volume (p3003–p3110, `--halves`) and the Sonnet
corrections pass of vols. I–II started at the end of session 1 (see Runs for what finished).
Next steps (exact commands; `$B` = scratchpad dir with page images: `python3 tools/drive_cache.py fetch
wip/embassy-to-china-staunton/source.json $B/pages`):
1. Finish any draft pages missing (resumable; skips done pages):
   `python3 tools/ocr_claude.py --model opus --prompt prompts/transcribe.md --images $B/pages --out $W/draft --pages 3003-3110 --halves --workers 8`
   and for p1008a, p2029a, p2029b (put only those three images in a directory of their own: `--pages 1008` would
   also take the hidden tissue leaf p1008), then `python3 tools/normalize.py $W/draft`.
2. Sonnet pass on every drafted page (resumable): `python3 tools/ocr_claude.py --model sonnet --prompt
   prompts/verify.md --images $B/pages --out $W/verify --corrections --context-text $W/draft --workers 8`
   (with no `--pages` it takes every image; the hidden leaves and covers have no draft — check that it skips them,
   or pass the list: vol. I/II leaves in `draft/`), then normalize, `review.py`, `judge.py` (workflow §3).
3. Scan checks: judge report; the singleton side-note variants (p1268, p1467, p2073, p2128, p2161, p2215,
   p2380, p2447, p2478, p2510: printed so, or misread?); tables (p1330, p1500, p2649–p2660, the plant lists).
4. Structure: two volumes as parts (`# Volume I` …), contents, divisions (front matter, lists of plates,
   appendix), placement of the folio plates (decide: a part of its own after vol. II, each plate with its
   engraved caption, the vol. I "List of the Plates" kept as their description — leaning, assumed).

## Leaf naming (several IA items in one book)
Vol. I IA leaf k = page file `p1000+k` (p1068 = IA leaf 68 = printed vol. I p. 24); vol. II IA leaf k = `p2000+k`;
the plates volume will be `p3000+k`. Working images: `$B/pages/` (built from `pages1/` and `pages2/` of
`prep_pages.py`, renamed; `leaves.json` there holds both items' leaf data). `book.json` `source.items` maps them back
to IA for scan links.

## Page map
Vol. I (from IA's numbering; to be completed from the scan check): p1001 cover · p1007–p1008 tissue guards (hidden) ·
p1009 title · p1011 advertisement · p1013–p1023 contents of vol. I · p1025–p10xx list of the plates in the folio
volume · p1068 = printed 24 (offset 1044) · printed 518 = last numbered page · p1568 back cover · p1569–p1573 IA
cards (hidden).
**Misbound in this copy:** p1467–p1468 are printed 425–426 and p1469–p1470 are 423–424: all present; `leaf_order` in
book.json puts them right.
Vol. II: p2001 cover · p2009 title · p2011 contents · p2024–p2025, p2334–p2335, p2646–p2647 reshoots IA hides
(hand in frame; good shots beside them) · printed 626 = last numbered page · appendix with tables at the end
(p2648 ff.) · p2666 back cover · p2667–p2671 IA cards (hidden).

**Missing from the UC scans, taken from the Getty copy of the same edition** (scan check 2026-11-20, subagent,
confirmed by me on p2029/p2030): vol. I frontispiece (portrait of Qianlong, List of Engravings no. I) = Getty vol. I
`gri_33125008481521` page n9 → `p1008a`; vol. II contents p. xx and text p. 1 (Chapter I heading) = Getty vol. II
`gri_33125008481786` n29, n30 → `p2029a`, `p2029b`. Fetched as single page images from IA (`/page/nN.jpg`; the
Getty text volumes are 8 GB archives); `book.json` `source.extra_leaves`. Say so in `notes_on_text`.
Vol. I page map (scan check): p1045 = printed 1 (leaf = page + 1044); chapters II p1074, III p1097, IV p1130,
V p1186, VI p1235, VII p1272, VIII p1362, IX p1427, X p1482; p1562 = p. 518 "End of the First Volume"; p1563–p1567
endpapers, labels. Front: p1011 advertisement, p1013–p1023 contents, p1025–p1039 list of the folio plates,
p1040–p1044 list of engravings in the quarto volumes. In-text engravings: p1185, p1243, p1385, p1397, p1469, p1487.
Tables: p1330, p1500.
Vol. II: p2008 frontispiece (Macartney); p2009 title; p2011–p2029 contents (p2024–p2025 reshoots, hidden);
p2030 = p. 2; p2497 blank back of plate, p2498 plate "Camellia Sesanqua" facing p. 467; p2649–p2660 appendix pp.
615–626 (p2658 a sideways table); p2660 "Finis"; p2661–p2665 endpapers, labels. Chapters II p2110, III p2196,
IV p2305, V p2370, VI p2468, VII p2558, VIII p2627. In-text engravings: p2039, p2101, p2113, p2141, p2157, p2233,
p2263, p2271, p2333, p2341, p2377, p2381, p2389, p2393, p2419, p2427, p2457, p2513, p2549, p2623.
Plant lists and tables: p2193–p2195, p2217–p2225, p2302–p2304, p2465–p2467, p2556–p2557.

**Illustrations** (cropped 2026-11-20 by an Opus subagent; every crop looked at on its contact sheets by me): 82
pictures from 80 leaves plus `images/cover.jpg` (vol. I title page), in `images/`; boxes in the session scratchpad
`crops.txt` (not kept). Two UC leaves were cut off at the edge of the scan, so their pictures come from the Getty copy
of vol. II: `p2008-1.jpg` (Macartney frontispiece, Getty n7) and `p2498-1.jpg` (Camellia Sesanqua, Getty n503); the
page files still come from the UC leaves. Folio plates in two halves are cropped as two images (p3007/8, 3015/16,
3021/22, 3025/26, 3031/32, 3035/36, 3039/40); after rotation by 90° (p3031/32, p3035/36, p3039/40) the
higher-numbered leaf is the upper half. A narrow strip at the fold is missing in p3025/26 (letters lost: "C" of
Macartney, "e of" before "the Hindostan"); say so in `notes_on_text`. p3056 (weapons) keeps its caption and key (they
cannot be separated). Say in `notes_on_text` which pictures come from the Getty copy.

## Decisions
- Side-notes: the book prints a marginal title beside the first line of most pages (repeated from page to page
  while the topic lasts), with a rule under it. Transcribed as `[[side: …]]` before the first word of the line it
  stands beside; the rule is not transcribed. In the JSON; left out of the editions (Tom).
- Printing: Bulmer's types, no long s, no catchwords seen so far; old spellings (enterprize, expence, mandarines,
  tho) are kept as printed.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Sample (draft + Sonnet) | 2026-11-20 | Opus / Sonnet | 12 | 0.90 + 0.44 | side-notes and old spellings right; Sonnet proposed no change |
| Draft vols. I–II | 2026-11-20 | Opus | 1,210 (incl. the sample) | 82.33 | 0 errors, 0 refusals |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
