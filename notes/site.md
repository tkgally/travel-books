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
