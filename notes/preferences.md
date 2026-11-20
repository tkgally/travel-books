# Tom's decisions

## 2026-11-19 (project set-up)

- **Purpose:** a long-term, open-ended public project: highly accurate and readable digital versions of
  first-person nonfiction travel books written and published in English before 1914, given to the public
  domain; a resource for modern readers to discover such books, enjoy them, learn from them and do research.
  No fixed goal; months or years. He will publicise it after a few weeks and may then get a domain name
  (so: relative links everywhere).
- **Selection:** the four conditions in `selection.md`, "for the time being". Books are chosen by Claude,
  usually alone by its own judgement and taste, sometimes after consulting him. Priority: a variety of
  interesting, readable books not easily available except in libraries or scans.
- **Print-on-demand facsimile reprints do not count** as post-1914 editions; real new editions do.
- **Text:** faithful; clear misprints corrected and recorded; line-end hyphenation resolved; illustrations and
  captions included; footnotes linked; **modern conventions for spacing around punctuation**.
- **Licence:** CC0 for everything — texts, JSON, site text, tools, prompts, notes.
- **Models:** Claude models through his subscription. Routine runs on Opus, which may give work to Haiku,
  Sonnet or Opus subagents or headless instances. **Fable only with his explicit permission** (the set-up
  session ran on Fable by his choice). Other companies' models through OpenRouter only for a second opinion on
  difficult scans, **at most $3.00 a day**.
- **Workflow:** starts from the English workflow of his pdf-to-epub project and is improved continuously and
  independently here, including the improvement process itself. That repository is private and is not
  attached to routine sessions: nothing here may depend on it.
- **Revisions:** published books may be revised when errors are found, and redone when a cleaner scan turns
  up, the workflow has improved enough to correct a significant number of errors, or the style rules have
  changed enough that the difference shows.
- **Site:** landing page with the published books and the queue; a page per book (bibliography, brief
  summary, EPUB and ODT downloads, HTML by chapter, link to IA and a page viewer if possible, link to the
  JSON); the JSON is the base of the other formats and holds the parts left out of them; the same text and
  paragraph styles for all books, with additions per book only when needed; shared CSS (and JS only if
  needed); no external dependencies; plain, minimal text with nothing that sounds like publicity; a
  straightforward, accessible, easily navigable, responsive design that does not try to catch the eye.
  Later perhaps: a topical index, other features.
- **Files:** IA files are fetched once and kept in his Google Drive folder "Travel Books" to spare IA's
  servers and the repository; working set in parts of at most 3 MB (the connector's limit).
- **Routine:** a scheduled routine points a session at `RESUME.md`, once or twice a day at first; he adjusts
  the frequency after watching token use — so say what each session cost.

## 2026-11-19 (answers after set-up)

- **Exclude books still in copyright where the term is life plus 70 years** (his example: in copyright until
  2037). Rule as recorded in `selection.md`: every author dead more than 70 years. *A Sportswoman in India*
  (Savory, d. 1966) moved to `rejected`.
- **Regularize the capitalization of titles to upper and lower case** (headings such as CHAPTER IV. →
  Chapter IV.). Recorded in `style.md`; I extended it to chapter summaries and captions printed in capitals
  (assumed).

## 2026-11-19 (later the same day)

- Confirmed: captions and chapter summaries in upper and lower case too; the embedded IA page viewer is fine.
- **Italics:** preserve them in the JSON, but in the built versions render them as roman in long extended
  passages, such as entire paragraphs or tables of contents. Rule and thresholds: `style.md` §Editions.

## 2026-11-19 (answer on the Rajah of Kolhapoor diary)

- **Publish *Diary of the Late Rajah of Kolhapoor*.** And as a standing rule: **a person whose date of death is
  unknown is assumed to have died before the age of 100.** Recorded in `selection.md` rule 5 (with my reading:
  the birth year must still be known or bounded, e.g. from a career; otherwise the book is left out).

## 2026-11-19 (during the South by West session)

- **Skip *South by West* (Rose Kingsley) for the time being, and try it again in the future.** A problem had
  occurred: the output filter refused three pages of the draft. Queue row `waiting`; resume steps in its log.
- **Do not choose books by the author's gender.** The queue has come to have mostly women authors; those books
  can all stay, but from now on choose without preferring any group: the aim is a wide range of authors,
  nationalities and destinations, with no particular ones preferred. Recorded in `selection.md` §"Choosing among
  those that qualify" and in the `select-book` skill.
- **Next session: take the next book from the queue as normal** (asked whether to first look for candidates by
  other kinds of authors, since five of the twelve queued books are by women: no).

## 2026-11-19 (answer on the refused pages; recorded later from the session transcript)

- Asked whether a session may type the pages the output filter refused, Tom answered: **"Yes, try typing those
  pages, both in this book and the previous one that got blocked."** The session that received this died trying
  (the filter ends a session that types such a page), and its note of the answer was never committed. What stands
  from the answer: both *Flying Leaves* and *South by West* are to be finished, not left waiting; their queue rows
  are `in progress` again. How: `tools/ocr_fallback.py`, not typing (CLAUDE.md, the output filter).

## 2026-11-19 (diagnosis of the first routine sessions)

- Tom asked a session (run on Fable by his choice) to look at the day's Opus sessions, find what caused their
  problems and redesign the workflow to avoid them. What was found and changed: `improvement.md` review log.
  Two changes touch rules he set, for him to confirm or reverse (below).

## 2026-11-19 (answers to the three questions of the diagnosis session: yes to all)

- **The checks rule as rewritten stands:** a session may fix a check that is wrong about a kind of book (test with
  invented text first) but does not publish that book; the next session does. (CLAUDE.md.)
- **Pages the output filter refuses may be published from the fallback:** tesseract's reading corrected by Opus,
  then the Sonnet pass, the judge and the audit; the book says which pages in its notes on the text.
- **The death-date rule keeps the added condition:** unknown date of death = died before age 100, provided the
  birth year is known or bounded (e.g. from a career); otherwise the book is left out. (`selection.md` rule 5.)

## 2026-11-19 (tables of contents)

- **Tables of contents are decided book by book.** Basic policy: follow the format of the printed book's contents,
  but deviate from it where the digital version would be easier to read with a different format. The same
  principle applies to the HTML, the EPUB and the ODT. Entries are consistent within a book (his example:
  *Sketches Awheel* gave the chapter number and places for some chapters and only the number for others), and
  neither too many nor too few. Where the print has a single entry for a long text (his example: the body of the
  *Rajah of Kolhapoor* diary), the editions may add entries of the editor's own, such as spans of dates and the
  places visited. How: `workflow.md` stage 4 "Contents", `book-json.md` (`toc`, `toc_entries`).

## 2026-11-19 (Staunton's *Authentic Account of an Embassy … to the Emperor of China*, 1797)

- **Add the three IA items of Sir George Staunton's *An Authentic Account of an Embassy from the King of Great Britain
  to the Emperor of China* (London: G. Nicol, 1797) to the top of the queue**: `authenticaccount01stau` (vol. I),
  `authenticaccount02stau` (vol. II), `gri_33125008481562` (the folio volume of plates, Getty). They are long; several
  sessions may be needed.
- **Combine all three volumes into a single digital volume** (one book; the volumes as parts, the plates placed as the
  book directs or as a section of their own: decide when the plate volume has been looked at).
- **Leave out the marginal titles** (side-notes naming the place etc.) **in the built versions** (HTML, EPUB, ODT); as
  everywhere, the JSON keeps them.
- **An exception to the selection rules, by Tom's choice** ("these books might not meet the guidelines for inclusion
  in this project, but I have enjoyed reading it so we can make an exception"): not to be rejected for a reprint, an
  existing digital text, or for being compiled by Staunton from Macartney's and others' papers rather than a plain
  first-person narrative. The life-plus-70 rule is met (Staunton d. 1801; Macartney d. 1806; Gower d. 1814; the
  engravers and William Alexander, the draughtsman, all died long before 1955).

## 2026-11-20 (answer on running quotation marks, *Embassy to China*)

- **Running quotation marks:** in books where the opening quotation mark of a long quotation is repeated at the start
  of each line (common in 18th-century and earlier books), follow modern practice: keep only the opening and closing
  marks of the whole quotation.
- **Quotations of several paragraphs marked with quotation marks** (not set off by indenting or other formatting):
  follow standard modern practice: an opening mark at the start of each paragraph, a closing mark only at the end
  of the whole quotation.

## 2026-11-20 (answers on the *Embassy to China* assumptions, and text lost in the scan)

- **Confirmed** the session-2 assumptions for *Embassy to China*: engravers' and publishers' lines on plates left out;
  the letters lost at the fold of the coastal-views plate supplied; "pratique-boat" keeps its hyphen; the part title
  "The Folio Volume of Plates".
- **Text lost or obscured in the scan** (a short piece, typically a word or less), when no other scan or edition
  settles it — a standing rule for all books:
  - **cannot be inferred:** the gap is marked, in the JSON and in the built versions (e.g. square brackets);
  - **can be inferred reasonably well from the context:** the JSON marks the gap and says the letters are inferred;
    the built versions show only the inferred letters, with no sign that the scan was unclear or that they were
    guessed — for smooth reading.

## 2026-11-20 (the books of "Japan As They Saw It" join the project; session run on Fable by Tom's choice)

Tom gave a session the Sources page of his earlier project "Japan As They Saw It" (JATSI: descriptions of Japan by
American and British visitors, 1855–1912; 247 books, each with links to its Internet Archive scans). JATSI was
an initial inspiration for Travel Books. His instructions:

- **The JATSI books are to be added to Travel Books gradually, one at a time, at about one JATSI book for every
  three books added to the project.**
- **Say which books came from JATSI**, on the site, so that people who come across it know why the project will
  have a growing imbalance towards books about Japan (the imbalance itself is fine).
- **A separate, stored list of all the JATSI books** (bibliographic information and IA links). From it, a dozen or
  so **that meet most or all of the project's criteria** go into the main queue shown on the home page.
- **Non-JATSI books** are chosen for the queue by the policies already established.
- **The text policy is the same** for JATSI and non-JATSI books.
- Notes where appropriate that Tom Gally decided to add the JATSI books gradually.
- The same session: assess the state of the project and its workflows, improve where needed, and plan how the
  landing page is organized as the number of books grows. That session does not do the routine work of
  `RESUME.md`; the normal run resumes in the next session, on Opus as usual.

How this was carried out: `notes/jatsi.md`.

## 2026-11-20 (answers on the JATSI questions, and on links)

- **Links.** Wherever the project "Japan As They Saw It" is mentioned on the site, the name links to
  <https://www.gally.net/jatsi/index.html>. **Every link to an outside page (IA and all others) opens in a new
  tab or window; only links within the site stay in the same one.**
- **The pace is as understood:** JATSI, other, other.
- **JATSI books already on Project Gutenberg will be added eventually, digitized afresh by this project** (Gutenberg's
  data is not used). They can have lower priority than the others.
- **The non-narrative JATSI books also have lower priority.**
- **Round-the-world books with a short Japan section are treated like any other book of this project:** if they meet
  the project's criteria in other ways they are queued with normal priority (and marked as JATSI); if they do not
  meet the general criteria, lower priority, still to be done eventually.
- **The JATSI books are exempt from the 70-year rule** ("they should all be in the public domain in the US and Japan,
  and I want to be able to add links to our new digitized versions from the JATSI Sources page sooner rather than later").
- **The Thompson drawing is to be added to *Corona and Coronet*.** (So: a minor illustrator whose death date is not
  found does not keep a drawing out.) **The Sheldon book is exempt too** (its two-page introductory letter by Anna
  C. Hartshorne, d. 1957) and goes in the queue as appropriate.
- **The pace of the regular sessions may be picked up**, depending on how many tokens the project uses and on the
  models' efficiency in the months ahead: "I hope that the maturation of this project will not be 'years away'."
  (So nothing in the notes should plan on the lower-priority JATSI books being far off.)

## Questions for Tom

None open.
