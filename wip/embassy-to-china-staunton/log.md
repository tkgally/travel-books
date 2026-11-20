# An Authentic Account of an Embassy … to the Emperor of China — Sir George Staunton (1797)

IA: `authenticaccount01stau` (vol. I; UC Libraries; 574 leaves, 300 ppi), `authenticaccount02stau` (vol. II; UC
Libraries; 672 leaves), `gri_33125008481562` (folio volume of plates; Getty; 114 images; not yet fetched — its page
images are a 1.2 GB `_images.zip`, not `_jp2.zip`).
Eligibility: an exception by Tom's choice (`notes/preferences.md` 2026-11-19); rule 5 met (Staunton 1737–1801,
Macartney 1737–1806, Gower 1742–1814, William Alexander 1767–1816). The book page and `site/about.md` must say it is
included as an exception (queue note).

## Status
Stage reached (end of session 2, 2026-11-20): scan checks, structure, plate pages and metadata done; preflight
**FAIL only on `audit`** (everything else ok or a reviewed look list: the 31 `joins` are all real continuations — page
tops are flush, checked on the scan; the 27 `contents` items are the printed chapter summaries, false alarms; the
`folios` items are the vol. II restart and plate numbers). Tables checked on the scan by an Opus subagent (see
Decisions). Nothing half-finished.
**Next (session 3):**
0. Tables (Opus subagent, session 2; full report summarized here): fixed p2219/p2223 running marks in rows, p2658
   1793 Dutch 2,938,530 (column total agrees), p2659 Bohea 3¾d. (arithmetic agrees). **Still to do on the scan:**
   p2658 (the tea-ships table): the 1784 and 1785 columns are shifted by a row (1784: French 8/4,231,200, Imperial
   5/3,428,400, Hungarian blank; 1785: Danes 4/3,158,000, Dutch 4/5,334,000, French 4/4,960,000, Portugueze
   4/3,199,000, American 2/880,100, Swedes blank); 1791 Prussian 3/743,100 and Genoese 1/260 (not American, Spanish);
   1792 Prussian 1/5,070, Spanish 1/—; 1793 Tuscan 1/393,870 (not Portugueze); Tuscan dashes vs Portugueze blanks
   1786–92. Consider transposing p2658 (21 columns) to one row per year. Layout: p2303 plant list as a two-column
   table like p2302/p2304; p2650 bracket of Siou-jou and Cho-tao (3,000 each, 402,000 together). The printer's own
   sums (p2650 470,870; p2653; p2657; p2659 1787 bullion) are left as printed.
1. Plates without a caption (maps and charts, folding halves: p3007/8, p3015/16, p3018, p3021/22, p3028, p3031/32,
   p3035/36, p3039/40, p3064): read the engraved title on the plate and give the second half (or the single leaf) one
   `[[caption]]` with it, as done for p3025/26; the vol. I "List of the Plates" (p1025–p1039) helps to read them.
   Check "Wesern Gates" (p3058) on the plate.
2. Preflight; rendered look (book page, a vol. I chapter, a vol. II chapter with engravings, appendix tables, plates;
   narrow and wide); audit (`audit_sample.py --n 6`, every candidate on a crop), record in book.json.
3. `site/about.md`: say that this book is an exception to the rules (queue note); then publish (workflow §8).

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
- Running quotation marks (the printer repeats “ at the start of every line of a quotation): left out, the
  quotation's own opening and closing marks kept. **Confirmed by Tom 2026-11-20**, who added: quotations of several
  paragraphs marked by quotation marks follow modern practice (opening mark at each paragraph, closing mark only at
  the end of the whole quotation) — `style.md`. Found by
  the judge (p1410: the draft kept ten repeats, Sonnet dropped them, the judge sided with the draft).
- Side-notes: the book prints a marginal title beside the first line of most pages (repeated from page to page
  while the topic lasts), with a rule under it. Transcribed as `[[side: …]]` before the first word of the line it
  stands beside; the rule is not transcribed. In the JSON; left out of the editions (Tom).
- Printing: Bulmer's types, no long s, no catchwords seen so far; old spellings (enterprize, expence, mandarines,
  tho) are kept as printed.

- Session 2 scan checks (2026-11-20): judge spots and review list looked at on crops. Fixed: p1259 "stalks," (the
  judge's ";" was wrong), p1217 and p1397, p2528 folios (broken types: 173, 353, 496), p1437 "rcceived" marked
  `[[corr]]`, p2054 comma, p2009 "His Majesty's", p2095 "Colao" and p1503 "Chu-san" (line-end hyphens), italics on
  p2029a. Kept as printed: p1322 "but" (= butt), the ten one-off side-note forms (missing hyphens/stops are the print's).
- Side-notes always stand beside the first line of the page; three placed mid-line were moved to the line start.
- Quotations in this book: no inner closing marks were found (paragraphs already follow modern practice). Running
  marks also stood at the start of every table row of quoted tables (p2217–p2225, Parish's survey of the Great Wall):
  66 removed (`running-quotes.txt`, "table row"); the centred lines of p2217 are paragraphs and keep their marks
  (assumed).
- `<blockquote>` on 21 page tops (drafts set the continuation of a running-quoted passage as a block quotation): the
  book does not set quotations off, so removed; the pages join their paragraphs.
- Structure: printed contents pages made plain lines (chapter number and title `[[center]]`, summary paragraph);
  parts "Volume I" (p1045, the printed head "Embassy to China." stays under it), "Volume II" (p2029b), "The Folio Volume
  of Plates" (p3007, title mine); the Appendix stands after Volume II at the top level of the contents; `toc.subtitles
  all` (the printed contents give every chapter's title). One frontispiece per volume (`frontispiece` is now a list:
  compiler change with a test): Qianlong before the Advertisement, Macartney at the head of Volume II.
- Folding plate p3025/26 (five coastal views): one image per half, the five captions as one `[[caption]]` on the
  second half; "[e of]" supplied in brackets where the fold strip is lost (assumed). Engravers' and publishers' lines
  left out (assumed, said in `notes_on_text`). p2141 and p3010 hold two pictures each: two `[[image]]`s.
- `running-quotes.txt`: 6 random entries looked at on crops (p1150, p1198, p1364, p1410, p2219, p2483): all are
  repeats at a printed line start.
- `keep_hyphens`: p1032 (Cou-pe-koo), p1105 (pratique-boat, assumed), p1194, p1364, p1525.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Sample (draft + Sonnet) | 2026-11-20 | Opus / Sonnet | 12 | 0.90 + 0.44 | side-notes and old spellings right; Sonnet proposed no change |
| Draft vols. I–II | 2026-11-20 | Opus | 1,210 (incl. the sample) | 82.33 | 0 errors, 0 refusals |
| Draft plates vol. (`--halves`) + Getty leaves | 2026-11-20 | Opus | 108 + 3 | 10.27 | 0 errors |
| Corrections | 2026-11-20 | Sonnet | 1,321 | 43.32 | 131 changes (36 punctuation, 61 markup, 34 words); 7 not applied |
| Judge | 2026-11-20 | Opus | 70 spots on 54 pages | 2.48 | verified 44, draft 26; 56 to look at on the scan |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
