# Style: the text, the editions, the site

Changes to this file change every future book and may make earlier ones look different; note the date of each
change at the foot, and see `workflow.md` §"New version" for when earlier books are redone.

## The text (Tom, 2026-11-19)

- **Faithful.** The author's words, spelling, capitals and punctuation marks exactly as printed, including old,
  inconsistent and foreign spellings and place-names.
- **Spacing is modern.** No space before `; : ! ?`, none inside quotation marks, contractions closed up
  (`do n't` → `don't`), dashes closed up. `tools/normalize.py` does this after every model step.
- **Printer's errors.** Only the unmistakable are corrected: transposed or doubled letters, a repeated word at
  a line end, a dropped letter in a common word, wrong fount, a missing full stop at the end of a paragraph, a
  quotation mark plainly missing or doubled. Each as `[[corr printed|corrected]]`. Not corrected: anything
  that could be the author's spelling or usage, proper names, dates and figures (even if wrong), grammar,
  inconsistency between two acceptable forms. In doubt, leave it. An errata slip printed in the book is
  applied the same way, with a line in `notes_on_text`.
- Line-end hyphens are resolved (the compound keeps its hyphen if the book hyphenates it elsewhere, or if it is
  one of `to-day`, `to-morrow`, `to-night` and the like in a book of that period; otherwise joined).
- Quotation marks curly, as printed (single or double as the book has them). A quotation opened and never
  closed in print is left so unless it is plainly a slip (then `[[corr]]`).
- **Running quotation marks** (assumed 2026-11-20, put to Tom): older books repeat the opening mark “ at the start
  of every printed line of a quotation. Like line-end hyphens, the repeats belong to the printed line, not to the
  words: the quotation keeps its opening and closing marks, the repeats are left out
  (`tools/running_quotes.py`, which lists each one; the list is kept in the book's directory).
- Long s → s; ligatures fi, fl as letters; æ, œ kept. Greek and other scripts in the script. Illegible → `〓`
  (never published: resolve from another scan, or note it in `notes_on_text` and waive).
- Italics and small capitals as printed.
- **Headings and titles in upper and lower case** (Tom, 2026-11-19): a heading, chapter title or summary, or
  caption printed in capitals is typed with capitals only where ordinary title case has them (`# Chapter IV.`,
  `# Preface.`, `[[subtitle]] From Cairo to the First Cataract`; roman numerals stay in capitals; small words
  such as a, an, the, and, of, in, to, from, with stay lower case except first). The wording, spelling and
  punctuation are not changed. Book titles in `book.json` likewise. Captions are my extension of his
  instruction ("titles"): assumed. Text printed in capitals inside a paragraph stays as printed.
- Footnotes keep the book's marks. Illustrations are placed where the book has them (a plate facing a page:
  after the paragraph in which the facing page ends), with their printed captions.

## What goes where

| Part | JSON | HTML / EPUB / ODT |
|---|---|---|
| Cover, half-title, title page, imprint, frontispiece caption | yes (kind `front`/`titlepage`) | a generated title page; the frontispiece itself is shown at the start of the first reading division |
| Dedication, preface, introduction, chapters, appendices, author's notes, glossary | yes | yes |
| Printed contents, list of illustrations | yes | no (a generated contents replaces them, decided book by book: `workflow.md` stage 4 "Contents") |
| Index | yes, page numbers tagged `<pref>` | no |
| Errata slip | yes | no (applied) |
| Publisher's advertisements, library book-plates and stamps | advertisements yes; library marks no | no |

Say what was left out in `book.json` `omitted_from_reading`. A long appendix of tables or documents may be
left out of the reading editions if it is not narrative; say so.

## Editions

- All books share `site/assets/book.css` (web and EPUB) and the named styles of `tools/render_odt.py`. A book
  gets `css_extra` only when its text needs a style the others do not have; if two books need it, it moves
  into the shared file.
- **Long italic passages are set in roman in the HTML, EPUB and ODT; the JSON keeps the italics as printed**
  (Tom, 2026-11-19: "long extended passages, such as entire paragraphs or in tables of contents"). The rule
  is applied by the renderers (`render_html.roman_long_italics`), never in the page files: a wholly italic
  paragraph, quotation or note of 30 words or more; a wholly italic piece of verse of four lines or more; a
  chapter summary; a table set all in italic. "Wholly" = at least 90% of its letters; the few words the print
  set in roman inside such a passage, for contrast, become italic. Shorter italics stay. The thresholds are
  mine: change them in one place if books show they are wrong.
- Web: one page per division; page numbers of the printed book hidden until the reader asks, each linking to
  that page of the scan at IA.
- EPUB: EPUB 3, epubcheck-clean, page list, pop-up footnotes. ODT: real footnotes, bookmarks at page starts.

## Site text

Plain and minimal. Say what the thing is; a reader should learn the facts and decide for themselves.

- **Summary of a book** (`book.json` `summary`, 60–150 words): who the author was (a clause), when and where
  they went and how, what the book contains, anything a reader should know before starting (dialect,
  attitudes of the time stated factually, missing maps). No adjectives of praise ("fascinating", "vivid",
  "remarkable", "delightful"), no "takes the reader", no rhetorical questions, no claims about importance
  unless a fact supports them (e.g. "the first account in English by an Indian visitor" only if established).
- Titles in the lists: short title, author, year. Regions as plain modern names, with the period name in
  `notes_on_text` if it helps.
- No exclamation marks, no second person, no calls to action beyond the link itself.

## Changes

- 2026-11-19: first version.
- 2026-11-19: headings, chapter titles and captions in upper and lower case, not as printed in capitals (no book yet published, none to redo).
- 2026-11-19: long italic passages roman in the built versions, italic in the JSON.
