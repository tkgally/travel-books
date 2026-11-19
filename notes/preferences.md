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

## Questions for Tom

- **2026-11-19, *Diary of the Late Rajah of Kolhapoor* (1872): may it be published?** The Rajah died in 1870.
  The editor, Capt. Edward W. West of the Bombay Staff Corps, Assistant Political Agent at Kolhapoor, was a
  captain by 1870 (about twelve years' service), so born about 1840 or earlier; he cannot have been alive in
  1955. But no source found gives his death date, and `selection.md` says "Death date unknown: establish it
  from a reliable source or leave the book out." The book is finished and passes every check (audit 30/30).
  Yes = publish it, and the rule could read "or the dates of the author's career put death before 1956 beyond
  doubt"; no = it goes to `rejected`.
