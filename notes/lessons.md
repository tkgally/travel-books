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
| A frontispiece left in the front matter, so missing from the reading editions [first book, 2026-11-19] | book.json `frontispiece`; test (set it whenever the book has one) |

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
- A model that returns "no corrections" in a few seconds may still be right: the audit's planted errors say
  whether that reader can see (first calibration: Sonnet 27/30, Opus 30/30).

## Trigger: plates (tipped-in leaves) and a frontispiece

- Preflight `conservation` cannot yet follow images the compiler moves: a plate between two pages of one paragraph
  (put after the joined paragraph) and a captioned `frontispiece` (put at the start of the reading text). Found in
  *Sketches Awheel* (2026-11-19); fix the check in a session that is not publishing such a book (plan in that
  book's log). A waiver is no substitute: the check reports only the first difference in a long text.
- Plates printed sideways: `crop_image.py --rotate 270` when the caption reads bottom to top along the right edge.

## Trigger: drop capitals at chapter openings

- Drafts type the capitals after a drop capital as small capitals (`T<sc>he</sc>`) on some chapters and as capitals
  on others; in both books so far the print had full capitals. Look at two openings on the scan and make all agree.

## Trigger: footnotes

- A note continued over the page arrives as a note with a new mark and no reference: make it `[[fn cont]]`.
- A signature under a note goes inside the note.
- Two marks in the text for one printed note: the second is `[[fnref * again]]` (the compiler warns "has no note" otherwise).

## Trigger: appendices, documents, quoted articles

- Each appendix as `## I. Title` in one Appendix division: `[[subtitle]]` after `##` renders as a plain paragraph.
- Drafts type running heads ("APPENDIX.") as `#` headings on every page: list all `#` lines and delete them.

## Trigger: verse and quotations over page breaks

- `[[cont]]` goes on the first line inside the second block, not before `<blockquote>`.
- A sentence that resumes after a set-off block at a page top must not get `[[cont]]`: it would be joined to
  the paragraph before the block [p2e].

## Trigger: index or in-book page references

- Drafts already tag some numbers: a blanket regex double-wraps them. Do not tag years.
- Set `[[page N]]` to the true number where the folio is misprinted, and say so in the log.

## Trigger: Google scan (`…goog` identifiers)

- Often bilevel, with folded maps unopened and occasional pages with a hand over the text: the scan check
  must look at every sheet at a size where that would show.

## Trigger: output filter

- The API's output filter can refuse ordinary pages: 3 of 413 in *South by West* (1874), e.g. p0076, a plain
  description of a shanty. No retries in the same session (RESUME.md); note the leaves in the log. Tom set the
  book aside (2026-11-19) rather than have the session type the pages: ask before choosing that route again.
- Second case: 5 of 304 in *Flying Leaves* (1885) in two runs of consecutive leaves (p0116–p0118, p0128–p0129:
  plain prose about German farmers in Wisconsin). A retry in a later session refused all five again: the
  refusals follow the page, not the time of the run, so one retry is enough to know. The tools no longer retry a refusal (`tools/refusal.py`), and preflight `leaves`
  lists leaves with no page file: a refused page must not slip into a published book unnoticed.

## Trigger: OpenRouter

- Check every `log.jsonl` for `finish` other than `stop` (some models' filters truncate silently) [p2e].
- Model names change monthly: read `/api/v1/models` first.

## Environment

- `tools/setup_env.sh` first (it switches apt to https mirrors: plain-http mirrors hang behind the session proxy). Headless calls: `claude -p` with only the Read tool (`ocr_claude.py`).
- Drive: uploads from a session are refused above about 3 MB per call (tested 2026-11-19: 2.86 MB went
  through; 9.9 MB and 40 MB did not). Downloads by `curl` with the file id work for any size because the
  folder is shared by link. The connector lists a folder a few files at a time: follow `nextPageToken`.
- www.gutenberg.org answers 503 to scripts; use the catalogue file. The Wikisource API rate-limits.
- IA: one download at a time; a 126 MB page-image zip took 14 seconds.
- `prep_pages.py` on 270 leaves: about a minute on 4 cores; 52 MB at the default size (19 Drive parts).
