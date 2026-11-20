# The site as it grows

What the pages are, how the home page changes as books are added, and what to do at each size. The builder is
`tools/build_site.py`; the tests are `SiteLists`. Tom's brief for the site is in `preferences.md` (2026-11-19:
plain, minimal, accessible, no outside dependencies, "later perhaps a topical index"); on 2026-11-20 he asked
for a plan for the home page as the number of books grows. This is it. Change it when the site shows it is wrong.

## Pages

| Page | What | Built from |
|---|---|---|
| `index.html` | what the site is (two short paragraphs); the books; the queue | `books/*/book.json`, `data/queue.json` |
| `places.html` | the books by part of the world; a book is listed under each part it covers | `regions` in `book.json` + `data/places.json` |
| `dates.html` | the books by the decade in which the journey began (first year in `period`; else the year of publication) | `period`, `year` |
| `authors.html` | the books by author, under letters — only when the home page no longer lists every book | `authors[0].sort` |
| `japan-as-they-saw-it.html` | why some books come from the JATSI list; those published and queued; the whole list with scan links | `data/jatsi.json`, the queue |
| `about.html`, `json-format.html` | | `site/*.md` |
| `books/<id>/…` | a book's page, its chapters, EPUB, ODT, JSON | the book |

Every line for a book, in every list, is the same (`book_line`): short title, author, year; under it the places,
the time of the journey, and "from Japan As They Saw It" for a book of that list.

## Stages

| Published books | Home page | To do when the stage is reached |
|---|---|---|
| up to 30 (`HOME_FULL_LIST`) | every book, by author; a line linking the lists by place and by date; the whole queue | nothing: this is now |
| 31 to about 150 | the ten newest (`HOME_NEWEST`, by date of version 1) and links to the three full lists; the whole queue | automatic. In the review session after the thirtieth book: look at the home page and the three lists on a narrow and a wide screen; move the queue to a page of its own (`queue.html`, one line on the home page) if it has more than about 25 rows |
| about 150 and more | the same | a part of the world in `places.html` with more than about 40 books gets its countries as sub-headings (East Asia will be first, because of JATSI: Japan, then the rest); `dates.html` by decade stays. Consider one page per part of the world. Consider a search box only if Tom asks: it needs a script and an index file, and the rule is "JS only if needed" |

Not planned until a reader or Tom asks: a subject index (`subjects` in `book.json` is free text and would first
need a fixed list of terms, as `regions` has in `data/places.json`); feeds; covers in the lists (they would make
the home page heavy and the lists harder to scan).

## Rules for the lists

- A new place name in a book's `regions` must be added to `data/places.json` with its part of the world (the
  test `test_every_region_of_a_published_book_has_its_part_of_the_world` fails otherwise). Use the names already
  in the file where they fit; a region inside a country (Hokkaido, Colorado) is listed beside the country.
- The parts of the world and their order are the `areas` list of that file. Islands in mid-ocean visited on a
  voyage go under "Atlantic and Indian Ocean islands" so that a voyage to China is not listed under Europe for a
  call at Madeira.
- `period` must contain a four-digit year for the book to fall in the right decade.
- The lists have no script: they are plain pages of links, each with a row of in-page links to its headings.

## The JATSI books on the site (Tom, 2026-11-20)

The reader is told in three places, in plain words: the second paragraph of the home page; the label
"from Japan As They Saw It (about these books)" on each such book and queue row; and the row "Why it is here" in
the table on the book's own page. Wherever the name stands in running text or a label it links to Tom's project
(<https://www.gally.net/jatsi/index.html>; `jatsi_name()` in the builder, a Markdown link in `site/*.md`), and
"about these books" links to the page on this site.

**Links** (Tom, 2026-11-20): every link to another site opens in a new tab or window (`target="_blank"
rel="noopener"`, added to every page by `outside_links` in `build_site.page`); links within the site do not.
The EPUB and ODT are not touched. `site/about.md` §"Which books" says the same. Nothing in
the reading text of a book differs.

## Display settings (Tom, 2026-11-20)

What Tom decided is in `preferences.md` (2026-11-20, "display settings"). How it is built:

- **One script, `site/assets/site.js`, in the head of every page, not deferred**, so that the colours are set before
  the page is drawn. It keeps one object in `localStorage` (`tb-display`, only the values that differ from the
  defaults) and the reader's places in another (`tb-place`: per book, the chapter file and the number of the block
  at the top of the window; the newest 100 books). Values read back are accepted only if they are in the script's
  own lists.
- **The script only sets attributes and custom properties on `<html>`** (`data-theme`, `data-font`, `data-align`,
  `data-para`, `data-corr`, `data-links`, `--tb-size`, `--tb-lh`, `--tb-width`, `--tb-ls`, `--tb-ws`, class
  `showpb`); the rules are at the end of `site.css` ("Display settings"). The text of the page is not changed, so
  a screen reader reads the same document. **`book.css` is not touched: it is shared with the EPUB.**
- **Without scripts** nothing of this exists: the "Display" button and "Continue reading" (book page) are made by
  the script, the chapter pages keep the page-number checkbox (the script removes it and offers the same in the
  panel), and the dark colours still follow the device (`prefers-color-scheme`, `:root:not([data-theme])`).
- **Scope** (Tom's second message, after seeing it): the button is on every page, to the right of "About". Colours,
  size, typeface, line, letter and word spacing, column width and link underlining apply to every page;
  justification, paragraph style and correction marks only to `article.book`.
- **Size:** `--tb-size` multiplies the root font size, so everything in `rem` grows with it (the column width too:
  the number of letters in a line stays about the same). **The header, the breadcrumbs and the panel follow it only
  up to 1.4, the sixth of the nine sizes** (`--tb-hs`; their font size is `1rem * hs / size`, and the panel's
  measures are in `em` for that reason). The side padding of the page does not grow. New rules for the site pages
  should use `rem` or `em`, not `px`, or they will not follow the setting.
- **The panel:** basic (colours, size, typeface, line spacing) and, behind "More settings", advanced (width,
  justified/ragged, paragraph style, letter and word spacing, four on/off buttons, reset). Controls are pictures;
  each has an `aria-label`, and the same words appear as a tip under it for a mouse (`hover: hover`) or keyboard
  focus. Radio groups are real radio buttons; steppers announce the new value in a `role="status"` element.
- **A new theme** needs its six colours in `site.css` (`:root[data-theme="…"]`), a swatch (`.tb-sw-…`) and its name
  in `CHOICES.theme` in the script; the dark colours are written twice (device and choice) and a test keeps the two
  the same. Print always uses black on white.
- **Not built, by Tom's decision:** hosted fonts (so no named fonts or weights), free choice of colours,
  pagination, scrolling settings.
- **Checked in Chromium only** (desktop and phone widths, scripts off, dark device). Not checked: Safari, Firefox,
  and real screen readers (VoiceOver, NVDA, TalkBack) — Tom or a reader must try those.
