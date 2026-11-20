# Workflow (current method)

`$R` = repo root, `$S` = session scratchpad, `$W` = `$R/wip/<slug>`, `$B` = `$S/<slug>` (bulky files).
Started 2026-11-19 from the English pipeline of Tom's private pdf-to-epub project; that project's evidence
is cited as "p2e".

## Choosing the pipeline

| Stage | Who | Why |
|---|---|---|
| Draft, every page | Opus, headless, `prompts/transcribe.md` | most accurate single reader in p2e's benchmarks |
| Corrections pass, every page | Sonnet, headless, `prompts/verify.md` (replies with a corrections list) | a differently biased second reading; cheap; catches dropped lines and duplicated passages |
| Judge, every spot where the two differ in words or punctuation | Opus, fresh call, readings labelled A/B blind | settles most disputes without the session reading every page |
| Scan check of what the judge leaves open | the session, on crops (`crop_spot.py`) | judges are wrong 1 time in 6–30 (p2e) |
| Audit, 6 random pages with planted errors | Opus, fresh call | measures the text and the reader's recall |

Calibration on this project's first scan (1880 London printing, 6 pages, 2026-11-19): proofreading with planted
errors, Opus found 30/30, Sonnet 27/30 (missed two dropped small words and one punctuation mark); the Sonnet
corrections pass proposed no change to the Opus draft, and the audit found no real error. So on clean
Victorian printing the draft is nearly right and the later stages are a net, not a rewrite.
API-equivalent cost per page: draft ≈ $0.07, corrections ≈ $0.035, audit ≈ $0.06 per audited page.

To try when a book is harder (older type, poor scan, heavy italics): two independent drafts (Opus and Sonnet)
with Opus judging every difference (p2e's method for eighteenth-century books), or `--halves` on the draft.
Before changing who does what for all books: 12–16 pages, both pipelines, `tools/score.py`, result in
`metrics.md`. Never a single-model text; never the same model as writer and only checker; never Fable.

## Verification (why the steps are what they are)

| Mechanism | What it guards | Where |
|---|---|---|
| Tests — seconds, no model calls | the tools; every published book still compiles | `tools/run_tests.sh` |
| Preflight — one command, every mechanical check | the book: nothing lost between page files, JSON, HTML, EPUB and ODT; markup, spacing, quotes, notes, links, epubcheck, LibreOffice | `tools/preflight.py` |
| Sampled audit — planted errors | the text against the scan, and the reader's own recall | `tools/audit_sample.py` |
| Source of truth in git | corrections and rebuilds need no model calls | `books/<slug>/pages/` |
| Records | the method itself, over time | `errata.md`, `metrics.md`, `lessons.md` |

Rules: (1) a check is not changed by the work it judges — see "When a check is wrong" below; (2) three
attempts at a cause, then the book goes to `waiting`; (3) new checks start in `observe` and
are promoted when `metrics.md` shows their alarms are mostly real; (4) every miss becomes a check, a test,
or a line in `lessons.md`, in that order of preference, in the session where it is found; (5) prune: lessons
a tool enforces are deleted; (6) tools change only with tests; (7) cheap checks first.

### When a check is wrong

Two of the first three books were held up by a preflight item that was the check's mistake (a second mark for
one note; plates moved by the compiler). What to do, so that neither the book nor the session is stuck:

1. Be sure it is the check: the page files say what the scan says, and the difference comes from something the
   tools do on purpose.
2. One item → a waiver in `book.json` (`check`, `match`, `why`) and publish; note it in `metrics.md`.
3. A kind of book (a waiver would be wide or would hide other items) → finish the book's other steps (audit,
   rendered look as far as possible), write "ready to publish when check X is fixed" and the cause in its
   log, leave the queue row `in progress`. Then, in the same session if there is time:
   - write a test with invented text that shows the false alarm (it fails), and where possible one showing
     that the fault the check exists for is still caught;
   - change the check; `tools/run_tests.sh` OK; `preflight.py` on every book in `books/` gives the same
     verdict as its stored stamp;
   - commit the check and its test on their own, with a row in `metrics.md` §"Preflight checks".
4. The session that changed the check does not publish the book it was changed for. The next session runs
   preflight and publishes.

## 0. Environment (once per container)

```bash
$R/tools/setup_env.sh $S/epubcheck          # tesseract, epubcheck 5.1.0, Pillow
export EPUBCHECK_JAR=$S/epubcheck/epubcheck-5.1.0/epubcheck.jar
$R/tools/run_tests.sh                       # must say OK
```
LibreOffice (`soffice`) is in the image; preflight needs it for the ODT check.

## 1. Start a book

1. Choose it (RESUME.md §2) and re-check eligibility (`selection.md` §"Before starting"). Set its queue row
   to `in progress`.
2. `mkdir -p $W`; write `$W/book.json` (keys: `book-json.md`; version 1) and `$W/log.md` from the template in
   `book-json.md`; `$W/source.json` = `{"ia_identifier": "…"}`.
3. Fetch once from IA into a directory of its own, make the working page images:
   ```bash
   python3 $R/tools/ia.py meta <identifier>
   python3 $R/tools/ia.py fetch <identifier> $B/src
   python3 $R/tools/prep_pages.py $B/src $B/pages           # pNNNN.jpg, 1800 px high, grey; leaves.json
   python3 $R/tools/contact_sheets.py $B/pages $B/sheets
   ```
   No `_jp2.zip`/`.tar` → another scan of the same edition, or the book is not eligible.
4. **Completeness and quality check — before anything is spent.** Look at ALL the contact sheets, and at full
   size at a dozen pages spread through the book plus anything that looks odd on the sheets. The scan fails if
   any page is missing (follow the printed page numbers through; `leaves.json` has IA's own numbering),
   duplicated in place of another, cut off, out of focus, hidden by a hand or a fold, or if a folding plate or
   map was not opened. A failed scan → try another IA scan of the same edition; none → queue row `rejected`
   with the reason. Write the page map in the log: leaf ranges for cover, front matter, contents, each
   chapter start if easy, plates, appendices, index, advertisements, blanks; printed-page offset.
5. **Cache in Drive**: create the folder `<slug>` in "Travel Books" with the Drive connector, put its id in
   `source.json` as `drive_folder_id`, then
   ```bash
   python3 $R/tools/drive_cache.py pack $B/pages $B/parts --source $W/source.json --extra $B/src/*_djvu.txt
   ```
   (leave out `--extra` if IA's OCR text is over 3 MB) and upload each listed part with the connector
   (`create_file`: `title` = part name, `parentId` = the folder, `contentMimeType: application/zip`,
   `disableConversionToGoogleType: true`, `base64Content` = the `sha256:…:path` string printed), recording
   each returned id: `drive_cache.py setid $W/source.json pages-003.zip <id>`. About 20 uploads for a 300-page
   book. Then delete `$B/src/*_jp2.zip` only after the full-size leaves for illustrations are extracted
   (step 6) — or keep it for the session.
   Later sessions: `python3 $R/tools/drive_cache.py fetch $W/source.json $B/pages`.
6. Full-size leaves for every page with an illustration, and for the cover:
   `python3 $R/tools/prep_pages.py $B/src $B/pages --full p0001,p0007,…` → crop now (stage 6 below) so that IA
   need not be asked again. If plates are found later that were missed, fetching from IA a second time is
   allowed; note it in the log.
7. Commit and push `$W` (book.json, source.json, log.md).

## 2. Draft

```bash
python3 $R/tools/ocr_claude.py --model opus --prompt $R/prompts/transcribe.md --images $B/pages --out $W/draft --workers 6
python3 $R/tools/normalize.py $W/draft
```
Leave out leaves that are not part of the book (colour card, covers without text, blank endpapers) with
`--pages a-b`; transcribe everything else, including contents, index and advertisements (they go in the
JSON). After the run: `log.jsonl` has no `error`; every page has a `.txt`; commit and push. The run is
resumable (finished pages are skipped), so a session that is cut off loses little.

**Pages refused by the output filter** (the run says how many; about 1 page in 100 so far, in runs of
consecutive leaves): do not retry and do not type them in the session (CLAUDE.md). Before `normalize.py`:
```bash
python3 $R/tools/ocr_fallback.py --images $B/pages --draft $W/draft     # the refused pages, from draft/log.jsonl
```
Tesseract reads each page and Opus corrects that reading against the image (a corrections list is not
refused). The page then goes through stage 3 like the others. These drafts start without italics, small
capitals, `[[cont]]` or note markup except what the corrector added, so: name the pages in the log
(`draft/fallback.json`), look at the Sonnet pass's changes on them with particular care, check their joins,
and add them to the audit (`audit_sample.py --pages …` as a second audit run). Say in `notes_on_text` which
printed pages were first read by OCR (`site/about.md` promises it). Tested 2026-11-19 on the five
refused pages of *Flying Leaves*: Opus and Sonnet both refused to draft them; both corrected the tesseract
reading without a refusal. A page refused here too stays without a file (preflight `leaves`) and the book
goes to `waiting`.

## 3. Corrections pass, review, judge

```bash
python3 $R/tools/ocr_claude.py --model sonnet --prompt $R/prompts/verify.md --images $B/pages --out $W/verify \
        --corrections --context-text $W/draft --workers 6
python3 $R/tools/normalize.py $W/verify
python3 $R/tools/review.py $W/draft $W/verify --out $W/spots.json
python3 $R/tools/judge.py --spots $W/spots.json --verified $W/verify --images $B/pages --out $W/judge
python3 $R/tools/normalize.py $W/judge
mkdir -p $W/pages && cp $W/judge/p*.txt $W/pages/
```
- `review.py`: look at every correction that was not applied, every length outlier, every page with an error.
- `judge/report.txt`: every "neither", every spot not marked sure, every case where the judge sided with the
  draft, and every change towards a more modern or more usual spelling is looked at on a crop
  (`crop_spot.py $B/pages/pNNNN.jpg 'three words there' $S/c.png`) and the page file in `$W/pages` edited.
  A subagent (Opus) can do a batch of these; it gets the crops, not the conclusion.
- From here `$W/pages/` is the text. Commit and push.

## 4. Structure pass (the session, in page order)

- Headings: one `#` per main division, matched against the printed contents; chapter summaries as
  `[[subtitle]]`; running heads gone. Models choose heading levels page by page: make them consistent.
- `book.json` `divisions`: front matter, title page, contents, list of illustrations, index, advertisements
  (kinds and which are left out of the reading editions: `style.md`).
- **Contents** (Tom, 2026-11-19, `preferences.md`): decided book by book, the same in the web pages, EPUB and
  ODT. Follow the printed contents; deviate where a reader of the digital edition is better served. Compile and
  print the entries (`python3 -c "import json,sys; sys.path.insert(0,'$R/tools'); import compile_book,
  render_html as rh; b,_=compile_book.compile_book('$W'); [print(n[0], len(n[3])) for n in rh.toc_tree(b)]"`)
  and look at them as a reader would:
  - alike within the book: every chapter with its summary or none (`"toc": {"subtitles": "all"}` when the
    printed contents gives them in full; a long summary otherwise drops from the entry);
  - neither too many nor too few: a long text with one entry (a diary, a journal, one long chapter) gets
    entries of the editor's, about one per 5–10 printed pages, at natural breaks: spans of dates and the places
    visited (`toc_entries`); sections the printed contents lists (appendices) get its titles (`"editor": false`);
  - parts nest their chapters; a part title with only a subtitle is still a part.
  Say in `notes_on_text` what the contents add to the print, and in the log what was decided and why.
- Page joins: preflight's `joins` and `hyphen-joins` lists; `keep_hyphens` for real compounds.
- Notes: marks pair up; a note continued over the page is `[[fn cont]]`.
- Printer's errors: `[[corr printed|corrected]]` only for the unmistakable (`style.md`).
- Spot-read against the scan every page with a table, verse, a letter, an inscription, or anything unusual.

## 5. Illustrations and cover

For each `[[image: …]]`: crop from the full-size leaf (`crop_image.py`, box in fractions of the leaf worked out
on the small image), save as `$W/images/pNNNN-k.jpg`, and look at every crop. Engravings and line drawings:
`--gray`. Longest side 1600 px, so a book with 100 plates stays under ~30 MB. `images/cover.jpg`: the front
cover if it is decorated, otherwise the title page. Alt text = the `[[image: …]]` description: say what is
shown, in a few plain words.

## 6. Metadata

Fill `book.json` (`book-json.md`): bibliographic fields from the title page (not from IA's catalogue record,
which is often wrong about dates and editions), author dates from a reliable source, regions, period of the
journey, the summary (`style.md` §Site text), `omitted_from_reading`, `notes_on_text`, `history`.

## 7. Build and verify

```bash
python3 $R/tools/preflight.py $W --report $W/preflight.txt
python3 $R/tools/build_site.py --out $S/site --bookdir $W        # then look at it in the browser build
python3 $R/tools/audit_sample.py --pages-dir $W/pages --images $B/pages --out $W/audit --rules $R/prompts/transcribe.md --n 6
```
- **Preflight must end PASS.** Fix causes in the page files; waive only what the scan justifies. Read every
  `look` list once: a real item there is fixed like any other. `leaves` is enforced: a refused draft page is never
  published. Leaves IA hides (`source.hidden_leaves`) do not count; any other leaf left out on purpose (an IA
  card) gets a waiver in `book.json` saying what it is, and a line in the log's page map.
- **Rendered look** (Playwright screenshots of `$S/site`): the book page, the first chapter, one with
  illustrations and notes, a late one; narrow and wide. Open the EPUB's chapters the same way if anything in
  the web pages looked wrong. Layout only: screenshots prove nothing about the text.
- **Audit:** look at every candidate it lists on a crop; about half are real (p2e). Fix the real ones. If
  recall on the planted errors is under 90%, the reader could not see the pages properly: say so in the log and
  treat "0 found" as unknown. Three or more real errors in the 6 pages → audit 20 more pages before
  publishing. Then record in `book.json`:
  `"audit": {"version": 1, "date": "…", "pages": 6, "recall": "29/30", "real_errors": 1, "fixed": 1}`.
- Re-run preflight after any edit.

## 8. Publish

1. `python3 $R/tools/publish.py <slug>` (runs preflight again; moves `wip/<slug>` → `books/<slug>`; queue row).
2. `log.md`: versions row with the preflight stamp and the audit result; waivers and reasons; known issues.
   `notes/metrics.md`: one row.
3. Tests, commit, push, PR, merge. When the Pages run finishes, open the live book page once.
4. Final message as RESUME.md §4.

## New version of a published book

Edit `books/<slug>/pages/` (or images, metadata); `version` + 1, new `date`, a `history` entry saying what
changed; preflight; an audit record for the new version (re-audit only if the text was re-transcribed —
otherwise copy the record with the new version number and `"note": "text unchanged except listed fixes"`);
`publish.py <slug>`; log, metrics, errata status. No model calls needed for corrections.
Reasons to redo a whole book (Tom, 2026-11-19): a cleaner scan is found; the workflow has improved enough that
a new pass would correct a significant number of errors; the style rules have changed enough that the book
visibly differs from newer ones.

## Not yet solved

- Marginal notes: solved 2026-11-20 (`[[side: …]]`, `page-markup.md`; tests `SideNotes`).
- Folding maps and large plates scanned in sections; two-page spreads.
- Eighteenth-century printing (long s, catchwords): the prompts say "long s → s, omit catchwords", untested
  here. Run the two-draft method on a sample first (p2e found Opus modernizes old spellings when drafting).
- Multi-volume works: one book id per work, volumes as parts; leaves named by item (`source.items` in
  `book-json.md`: vol. I p1000+, vol. II p2000+), tested on invented data only; the book page links and embeds every item.
- Endnotes printed at the end of the book rather than at the foot of the page.
- Greek, Arabic or other scripts quoted in the text: transcribe in the script; untested.
