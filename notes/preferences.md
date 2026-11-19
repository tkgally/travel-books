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

## Questions for Tom

- *A Sportswoman in India* (Isabel Savory, 1900): the author died in 1966. Public domain in the United States
  and Japan, in copyright until 2037 where the term is life plus 70 years. Publish, or keep to authors dead
  70 years? (Until answered: such books wait.)
- Headings are shown as printed, usually in capitals (CHAPTER IV.). Keep, or set in upper and lower case?
  (Assumed: keep.)
- The IA page viewer on each book page is an embedded frame from archive.org, loaded only when opened. It is
  the one piece of outside content on the site. (Assumed: acceptable, since he asked for a viewer.)
