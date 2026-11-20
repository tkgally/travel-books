# Lessons — a checklist keyed to what the book has

Read **Always**, then only the sections whose trigger matches the book. Every line is something that went wrong
once, here or in pdf-to-epub ("p2e", the private project this pipeline came from). Rules for this file: a
lesson a script can check goes into `tools/preflight.py` or a test instead, and is listed under "Now checked by
tools"; otherwise one or two lines under the right trigger; when a section passes ~12 items, merge or delete.

## Now checked by tools

| What went wrong | Caught by |
|---|---|
| Markup showing in the book; `〓` left in | preflight `markup`, `stray-markup` |
| Straight quotes | compiler; preflight `straight-quotes` |
| Notes without references and the reverse | compiler; preflight `compile` |
| Text lost or reordered between page files and an edition | preflight `conservation` |
| `[[cont]]` on a page that starts a new paragraph; missing `[[cont]]` | preflight `joins` (observe) |
| Misread or misprinted page numbers | preflight `folios` (observe) |
| Headings that differ from the printed contents | preflight `contents` (observe) |
| Small capitals typed as capitals; old spacing left in | `normalize.py`; preflight `sc-caps`, `spacing` |
| A builder change breaking an earlier book | test `Books` |
| Headings, chapter titles or captions left in capitals | preflight `heading-caps` |
| A missing illustration file crashing the EPUB build [found by the tests, 2026-11-19] | compiler warning; test |
| A finished book failing `conservation` because the compiler moved a plate or a captioned frontispiece [*Sketches Awheel*, 2026-11-19] | preflight compares image captions apart from the text; test `MovedImages` |
| A draft page refused by the output filter and left out unnoticed | `ocr_claude.py` says so at the end of the run; `ocr_fallback.py`; preflight `leaves` |
| A frontispiece left in the front matter, so missing from the reading editions [first book, 2026-11-19] | book.json `frontispiece`; test (set it whenever the book has one) |
| `setup_env.sh`'s https rewrite of the apt mirrors matched nothing (`\|` inside `s|…|`), so apt hung on plain http for 20 min [2026-11-19] | fixed; test `SetupEnv` |
| `drive_cache.py fetch --pages p2029b` refused leaves with a letter (added from another scan) [*Embassy*, 2026-11-20] | accepted; test `DrivePages` |
| `drive_cache.py fetch --pages a,b,c` read the list as one name and fetched the wrong parts without a word [2026-11-19] | lists and ranges accepted, anything else refused; test `DrivePages` |
| A part title with a `[[subtitle]]` ("Flying Leaves. / From the East.") taken for a chapter, so its chapters did not nest under it [*Flying Leaves*, found 2026-11-19] | compiler; test `Contents` |
| Side-notes (marginal notes) lost between page files and JSON, or shown in the editions [*Embassy to China*, 2026-11-20, before the first run] | preflight `conservation` (side-notes apart); test `SideNotes` |
| A paragraph moved by the verifier (before a picture → after its caption) judged one way at one end and the other way at the other, so `judge.py` dropped it [*Rambles*, p0092, 2026-11-20] | `judge.py` keeps the verifier's reading at both ends; test `test_judge_move_judged_both_ways_keeps_text` |
| A paragraph interrupted by an engraving in the middle of a page split in two (`[[cont]]` dropped) [*South by West*, 2026-11-19] | compiler joins it; test `ImageInParagraph` |

## Always

- **Never publish a single-model transcription.** Drafts run away, truncate, drop first lines, duplicate
  passages [p2e]. Two differently biased readings, differences judged.
- **Models silently restore what they think the text should be**: modern spellings, familiar place-names,
  regular grammar. The check is a second reading with a different bias, never the same model again [p2e].
- **Readers and judges are wrong about 1 time in 6–30** on the changes they propose [p2e]. A proposed change
  to a letter is looked at on a crop before it is accepted, above all one towards the more usual form.
- A page whose two readings differ in length by more than 5% needs a look (`review.py`).
- More reasoning effort is not better OCR; text-only clean-up without the image is not worth doing [p2e].
- Take the bibliographic facts from the title page, not from IA's record.
- Start the model runs first and do page-map work while they run.
- Screenshots are for layout only; preflight and the audit are for the text.
- Read the generated contents as a reader would before publishing: the first three books went out with
  chapter entries unlike one another (long summaries dropped) and a 90-page diary as one entry; Tom asked for
  contents decided book by book (`workflow.md` stage 4 "Contents") [2026-11-19].
- A model that returns "no corrections" in a few seconds may still be right: the audit's planted errors say
  whether that reader can see (first calibration: Sonnet 27/30, Opus 30/30).

## Trigger: plates (tipped-in leaves) and a frontispiece

- Decorative chapter head-pieces and tail-pieces: drafts mark each as `[[image:]]`; keep them, crop them, list them
  in `book.json` `ornaments` (shown small; Tom, 2026-11-20).
- A frontispiece printed sideways has no caption to show which way: crop it, look at both turns.
- Plates printed sideways: `crop_image.py --rotate 270` when the caption reads bottom to top along the right edge.
- Set `frontispiece` in book.json, with or without a caption (preflight follows moved images since 2026-11-19).
- A plate with a label or sub-captions on separate lines: one `[[caption]]`, parts separated by full stops; several
  `[[caption]]` lines fail preflight `conservation` (it compares caption lines; the compiler joins them) [*Corona and Coronet*, 2026-11-19].
- A folding map shot in two halves: crop each half; try joining them only if the shots overlap (they did not in
  *Corona and Coronet*: a strip at the fold was missing, said in `notes_on_text`).

## Trigger: eighteenth-century printing

- Quotations with “ repeated at every line start: models keep the repeats, which then stand mid-sentence once lines
  are joined; `tools/running_quotes.py` after the judge, its list looked at (*Embassy*, 2026-11-20). Only for a book
  that prints the convention: on *South by West* (1875) it lists 6 real opening marks that follow a quotation left
  unclosed earlier in the paragraph (p0091, p0092, p0107, p0290, p0347, p0406: printed so or a dropped ”? — to look at
  in the next review). Also at the next review: do the published books have quotations of several paragraphs with a
  closing mark at each inner paragraph (Tom 2026-11-20: modern practice, `style.md`)?
- Drafts set a page-top continuation of a running-quoted passage as `<blockquote>` (21 pages of *Embassy*); the book
  sets no quotation off, so the compiler found "[[cont]] with nothing to continue". Running marks also stand at the
  start of each row of a quoted table; `running_quotes.py` does not look in tables (*Embassy*, 2026-11-20).
- Scans of old multi-volume sets: the scan check found a missing first page of text and a missing frontispiece
  (UC copy) that IA's own page numbers did not show; another library's scan supplied them page by page.

## Trigger: drop capitals at chapter openings

- Drafts type the capitals after a drop capital as small capitals (`T<sc>he</sc>`) on some chapters and as capitals
  on others; in both books so far the print had full capitals. Look at two openings on the scan and make all agree.

## Trigger: a printed contents with chapter summaries

- Drafts type such contents page by page differently (`##` headings and `[[subtitle]]`s on some pages, tables on
  others), and `[[cont]]` lands mid-page after a heading. Make it plain lines as printed (`[[center]]` number and
  title, the topics as a paragraph ending in `<pref>`), drop "PAGE" heads and dot leaders [*South by West*, 2026-11-19].
- A page that starts flush left after a closed sentence is still a continuation (`joins` lists it): look at the indent.

## Trigger: footnotes

- A note continued over the page arrives as a note with a new mark and no reference: make it `[[fn cont]]`.
- A signature under a note goes inside the note.
- Two marks in the text for one printed note: the second is `[[fnref * again]]` (the compiler warns "has no note" otherwise).

## Trigger: appendices, documents, quoted articles

- Each appendix as `## I. Title` in one Appendix division: `[[subtitle]]` after `##` renders as a plain paragraph.
- Drafts type running heads ("APPENDIX.") as `#` headings on every page: list all `#` lines and delete them.
- Wide tables with blank cells (no dash) among dashed ones: drafts shift whole columns up or down a row (*Embassy* p2658,
  21 columns). Sum each column against the printed total by script, and read the blanks and dashes on a rotated crop.

## Trigger: verse and quotations over page breaks

- `[[cont]]` goes on the first line inside the second block, not before `<blockquote>`.
- A sentence that resumes after a set-off block at a page top must not get `[[cont]]`: it would be joined to
  the paragraph before the block [p2e].

## Trigger: index or in-book page references

- Drafts already tag some numbers: a blanket regex double-wraps them. Do not tag years.
- Set `[[page N]]` to the true number where the folio is misprinted, and say so in the log.

## Trigger: a book about Japan (the JATSI books)

- First one (*Rambles through Japan*, 1892, 2026-11-20): Kioto, Ozaka, Ko-ya-san, jinrikisha, *saké* all kept as
  printed; the only judge spot on such a word (*saké* vs *sakè*) the verifier had right on the crop; audit 30/30, 0
  candidates. Keep cropping every judge spot and audit candidate on a romanized word; Japanese script: none in it
  (`workflow.md` §"Not yet solved").
- The year of the journey is often not printed: work it out from weekdays given with dates and from what the
  traveller could use (railways), and say in the summary that it is inferred.

## Trigger: Google scan (`…goog` identifiers)

- Bitonal: halftones and many engravings come out blank. Good for supplying a missing leaf's text, not its picture
  (*Rambles* p. 114, 2026-11-20). Its page images are small (767 px wide): upscale to the working height.
- Often bilevel, with folded maps unopened and occasional pages with a hand over the text: the scan check
  must look at every sheet at a size where that would show.

## Trigger: output filter

- "Output blocked by content filtering policy" on a draft page: the refusal follows the page, not the model or
  the time (*South by West* 3 of 413; *Flying Leaves* 5 of 304, refused by Opus twice and by Sonnet). The
  pages are ordinary prose. `tools/ocr_fallback.py` is the route (workflow §2); the tools never retry.
- A session that set out to type such a page itself was ended by the same filter, and every later turn of
  that session failed at once (2026-11-19). Never do it, whoever asks; say why and use the fallback.
- The corrections pass, the judge and the audit were not refused on those pages.

## Trigger: OpenRouter

- Check every `log.jsonl` for `finish` other than `stop` (some models' filters truncate silently) [p2e].
- Model names change monthly: read `/api/v1/models` first.

## Environment

- CI (`pages.yml`) installs only Pillow before the tests: a test that needs another package must add it there (a test importing `crop_image` broke the deploy on 2026-11-19).
- `sleep` in a foreground command is blocked: run long commands in the background and do other work meanwhile.
- `publish.py` runs preflight again: `export EPUBCHECK_JAR=…` in the same command, or it fails on epubcheck.
- `tools/setup_env.sh` first (it switches apt to https mirrors: plain-http mirrors hang behind the session proxy). It
  takes a few minutes; preflight and the tests need only epubcheck and Pillow, so run it in the background. Headless calls: `claude -p` with only the Read tool (`ocr_claude.py`).
- Drive: uploads from a session are refused above about 3 MB per call (tested 2026-11-19: 2.86 MB went
  through; 9.9 MB and 40 MB did not). Downloads by `curl` with the file id work for any size because the
  folder is shared by link. The connector lists a folder a few files at a time: follow `nextPageToken`.
- www.gutenberg.org answers 503 to scripts; use the catalogue file. The Wikisource API rate-limits.
- IA: one download at a time; a 126 MB page-image zip took 14 seconds.
- `prep_pages.py` on 270 leaves: about a minute on 4 cores; 52 MB at the default size (19 Drive parts).
