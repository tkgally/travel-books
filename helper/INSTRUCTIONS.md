# Travel Books: instructions for a helper model

Version 2, 2026-11-25. Written by Claude, which manages the project for Tom Gally. If anything here is unclear or
turns out to be wrong, do what seems most sensible, and say so in your notes (step 8): these instructions are
revised after every job.

## What this is

*Travel Books* (<https://github.com/tkgally/travel-books>) publishes accurate digital editions of travel books
printed before 1914, transcribed from scans at the Internet Archive, in the public domain. You are asked to do the
**first reading** of one book: transcribe its pages, cut out its pictures, and describe the book in a small data
file. Claude then checks your work against the scan, corrects it, and publishes the book.

Two things matter more than anything else:

1. **The text must be what is printed, letter for letter.** A second reader will compare your text with the scan.
   Every word you "improve" (a modern spelling, a tidied comma, a name in its usual form) costs more to find and
   undo than a word you could not read and marked as doubtful. An old or odd spelling is the author's; leave it.
2. **Say what you did and what you are unsure of.** The notes you deliver are read as carefully as the text. A list
   of twenty doubtful readings is useful. A delivery that claims to be perfect, or that describes steps that were not
   actually done, is not.

Speed does not matter. Take the pages one at a time.

## Where things are

Tom gives you two files: a short `INSTRUCTIONS.md`, which says to read this one, and **one zip file for the book**,
`<date>-<book-id>.zip`. Unzipped, it is the folder `<book-id>-job/`:

```
<book-id>-job/
  JOB.md               what to know about this book: read it after this file
  job.json             the same facts for the checking tool
  book.json            the book's data file, partly filled in
  fetch_scans.py       downloads the page images (they are too large to be in the zip)
  scans.json           the list fetch_scans.py works from
  kit/
    INSTRUCTIONS.md    this file
    transcription-rules.md, page-markup.md, book-json.md
    sample-book/       a small invented book that shows the markup in use
    tools/             the programs you run: crop_image.py, normalize.py, helper.py, compile_book.py
```

Use only these files and the scans that `fetch_scans.py` downloads. Do not take text from the Internet Archive's
OCR, from another website or edition of the book, or from memory, and do not get the scan from anywhere else.

## The job, step by step

Work in a local folder. You need Python 3 with the Pillow library (`pip install pillow`).

1. **Set up.** In the job folder run

   ```
   python3 fetch_scans.py
   ```

   It downloads the scans in about thirty small parts, checks each, and unpacks them: `scans/pages/pNNNN.jpg`, one
   grey image per leaf of the scan, 1800 pixels high, and `scans/full/pNNNN.jpg`, full-size colour images of the
   leaves that have pictures and of the cover. If it fails, run it again; if it keeps failing, stop and tell Tom.
   Then make a folder named with the book's id (below: `BOOK/`) holding `pages/`, `images/` and a copy of the job's
   `book.json`. Read `JOB.md`, then `kit/transcription-rules.md` (the rules for the text and the page markup),
   `kit/page-markup.md` (the same markup as a table) and the pages of `kit/sample-book/pages/` (an invented book that
   shows the markup in use).

2. **Transcribe, one leaf at a time.** For every leaf in the range `JOB.md` gives, look at its image
   `scans/pages/pNNNN.jpg` and write `BOOK/pages/pNNNN.txt` (same number) following `transcription-rules.md` exactly. Every leaf
   in the range gets a file, blank pages too (`[[page ?]]` and `[[blank]]`).
   - Read the image itself, at its full resolution. If small type is hard to read (footnotes, an index, tables),
     enlarge that part of the image, or cut the page into overlapping halves, rather than guessing.
   - Write each page file from its image only. Do not carry text over from the page before; do not finish a sentence
     from what it ought to say.
   - Give each page your whole attention. Do not have many pages transcribed in one go by a quick process and then
     assume they are right.

3. **Proofread every page against its image**, as a separate second pass after the page is written (best after the
   whole book is written, so that you come to each page fresh). Read the image and the file side by side, word by
   word. Look hardest at: proper names and foreign words (letter by letter), numbers and dates, punctuation marks,
   where italics begin and end, the first and last lines of the page, lines dropped or doubled, and footnotes.
   Words that look modern or familiar in your file deserve a second look at the print.

4. **Go through the whole book in order**, as a reader would:
   - `[[cont]]` at the top of every page whose first paragraph continues the page before (no paragraph indent in the
     print), and nowhere else;
   - a word divided by a hyphen at the foot of a page: the hyphen stays at the end of the page file, as printed;
   - headings: one `# ` heading at each chapter or other main part, the same pattern for every chapter, matching
     the book's printed contents; a chapter's printed summary as `[[subtitle]]`;
   - every footnote reference `[[fnref *]]` has its note `[[fn *]]` on the same page, and the reverse;
   - a paragraph that a picture interrupts in the middle of a page: the part after the picture starts with
     `[[cont]]`.

5. **Cut out the pictures.** Every illustration in the leaf range (plates, pictures set into the text, maps,
   pictorial initials and head-pieces if `JOB.md` says so) has an `[[image: …]]` line in its page file and a file
   `BOOK/images/pNNNN-k.jpg` (the k-th picture on leaf pNNNN, counting from 1). Cut each one from the **full-size**
   image of its leaf:

   ```
   python3 kit/tools/crop_image.py scans/full/pNNNN.jpg BOOK/images/pNNNN-1.jpg x0,y0,x1,y1
   ```

   The box is in fractions of the leaf (0 to 1): left, top, right, bottom. The tool reduces the picture to at most
   1000 pixels on its longest side and saves it as a JPEG; use it for every picture, so that all are made the same
   way. Add `--gray` for line drawings and wood engravings; leave photographs and anything printed in colour or tint
   as they are. A plate printed sideways is turned upright with `--rotate 90` or `--rotate 270`.

   **Then open every picture you made and look at it.** It is right when:
   - the whole picture is there: nothing cut off at any edge, including lettering or a signature that is part of the
     drawing;
   - none of the page's text is inside it: no lines of the body text, no caption set in type (the caption is
     transcribed as `[[caption]]`, not kept in the picture), no page number or running head;
   - there is a small even margin of paper around it, and no dark edge of the page or of the book's gutter;
   - it is upright.

   If it is not right, change the box and cut it again, as many times as it takes. Where text is wrapped so tightly
   round an irregular picture that no rectangle avoids it, keep the whole picture, let in as little text as possible,
   and list the picture in your notes.

   Also make `BOOK/images/cover.jpg` from the leaf `JOB.md` names for it (the front cover if the title can be read on
   it, otherwise the title page), in the same way.

   The words after `[[image:` are a short plain description of what is shown (“A street in Oaxaca with a church
   tower”), for readers who cannot see the picture. Do not repeat the caption.

6. **Fill in `BOOK/book.json`.** The fields already filled in were checked by Claude: leave them. Add:
   - `divisions`: one entry for each part of the book that is not an ordinary chapter, `{"at": "pNNNN", "kind": …}`,
     where `at` is the leaf it starts on. Kinds: `front` (cover, half-title, anything before the title page),
     `titlepage` (always needed; `"title": "Title Page"`), `dedication`, `preface`, `contents`, `illustrations`,
     `introduction`, `part`, `appendix`, `notes`, `glossary`, `index`, `errata`, `advertisements`, `back`. Chapters
     need no entry: every `# ` heading starts a chapter unless an entry says otherwise. `kit/book-json.md` explains
     all the fields; `kit/sample-book/book.json` is an example.
   - `summary`: 60 to 150 words saying who the author was (a clause), when and where they went and how, and what the
     book contains. Plain statements only, taken from the book: no praise (“fascinating”, “vivid”, “remarkable”), no
     “takes the reader”, no claims about importance. Serial commas; curly quotation marks and apostrophes.
   - `period` (the years of the journey, e.g. `"1904–07"`), `regions` (modern country names),
     `omitted_from_reading` (leave the text the job gives unless the book differs), and `notes_on_text` (a list of
     plain sentences on anything a reader should know: a missing map, a damaged page; empty if nothing).

7. **Check it.**

   ```
   python3 kit/tools/normalize.py BOOK/pages
   python3 kit/tools/helper.py check BOOK --job job.json
   python3 kit/tools/compile_book.py BOOK
   ```

   `normalize.py` tidies spacing only. `helper.py check` must end `RESULT: PASS`: fix what it lists by looking at the
   scan again, never by changing text just to make a message go away, and look at each `WARN` line.
   `compile_book.py` writes `BOOK/<book-id>.json`, the book as one JSON file; it must report 0 warnings. Open that
   file and read one chapter through in it: text in the wrong order, a heading in the middle of a sentence or a
   paragraph broken in two shows up there.

8. **Write `BOOK/NOTES.md`.** Plain and specific. It must have:
   - which model you are, the thinking or effort setting, the date, and roughly how long the job took;
   - how you actually worked: how each page was read (the image directly? in parts? any OCR tool?), whether step 3
     was done for every page, anything you skipped or did differently from these instructions, and why;
   - **doubtful readings**: leaf, the words, and what the doubt is, for every place where you were not sure what is
     printed;
   - **printer's errors**: every `[[corr printed|corrected]]` you marked, and separately anything that looks like a
     printer's error but that you left as printed;
   - pages with anything unusual (tables, verse, columns, letters, another script, damage) and how you typed them;
   - pictures you are not satisfied with, and pictures where text could not be kept out;
   - what in these instructions, the rules or the tools was unclear, missing, wrong or got in your way.

9. **Deliver.** Make one zip file named `<book-id>.zip` whose top folder is `<book-id>/`, holding exactly:
   `pages/` (the page files), `images/` (the pictures and `cover.jpg`), `book.json`, `NOTES.md` and `<book-id>.json`.
   Nothing else: no page images from the scan, no scripts, no working files. Put it in the folder `Inbox` of the
   Google Drive folder "Helper model workspace" (or wherever Tom says), and tell Tom it is there. Do not publish anything, and do not send anything to the project's GitHub repository.

## The mistakes that matter most

From the first trial (a book done without these instructions). Its text was good: about as accurate as our own
first reading. These are the things that still had to be found and put right, in order of cost:

1. **A word made more usual without a mark.** “neophite” in the print was typed “neophyte”; a romanized Japanese
   phrase printed as two words was run into one; a hyphen at a line end inside a hyphenated word became a dash.
   These read perfectly and are the hardest errors to find. Type what is printed. Correct only an unmistakable
   printer's error (a turned or dropped letter in a common word, a doubled word), always as
   `[[corr printed|corrected]]`, and list every one in the notes. Never correct a proper name, a foreign word, a
   number, grammar, or anything that could be the author's own spelling. If in doubt, leave it and note it.
2. **Italic tags that take in punctuation that is not italic.** In `(<i>O-dah-wah-rah</i>),` the brackets and the
   comma are upright in the print, so they stand outside the tags. This was wrong about a thousand times in one
   book. Look at the shape of the brackets and stops next to italic words.
3. **Pictures cut carelessly**: many had lines of the page's text inside, or an edge or the lettering cut off.
   Step 5 says what a good picture is; every one is looked at after it is cut.
4. **Something printed on the page left out** (the book's title printed again above Chapter I). Everything printed
   is typed, except what the rules say to leave out (running heads, page numbers, signature marks, library stamps,
   lettering drawn inside a picture).
5. **A hyphen at the very end of a page dropped.** The last word of a page, if divided, keeps its hyphen.
6. **Matter set in columns typed as loose paragraphs.** A vocabulary or table printed in columns is typed as a pipe
   table, one printed row per line, the cells in the order they stand across the page, unless `JOB.md` says
   otherwise. Headings of the same rank in the print get the same number of `#`.
7. **No cover picture.**

Done well in that trial, and wanted again: lettering drawn inside pictures was rightly left out and captions set
in type were kept; printer's errors that were marked were marked correctly; the structure of the book (title page,
dedication, chapters, appendix) was right.
