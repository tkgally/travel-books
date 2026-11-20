# The JATSI books

"Japan As They Saw It" (JATSI, <https://www.gally.net/jatsi/index.html>) is an earlier project of Tom's:
passages about Japan by American and British visitors, with a Sources page listing 247 books (1855–1912) at the
Internet Archive. It was one of the starting points of this project. On 2026-11-20 Tom decided that those books
are to be added here gradually (`preferences.md`, that date). This file says how.

## What Tom decided

- One JATSI book at a time, at about one for every three books added to the project.
- The site says which books came from JATSI and why (the shelf will lean towards Japan; that is accepted).
- A stored list of all the JATSI books; a dozen or so that meet most or all of the criteria go in the main queue.
- Other books are chosen as before (`selection.md`). The text policy is the same for all books.

## Where things are

| What | Where |
|---|---|
| The whole list: number, year, title, author, JATSI's one-line summary, IA scans, Gutenberg numbers, `kind`, `hold` | `data/jatsi.json` (does not change when a book is queued or published) |
| A JATSI book's state | its row in `data/queue.json`: `"from": "jatsi"`, `"jatsi": <n>` |
| The pace | `queue.json` `jatsi_policy`; `python3 tools/ledger.py` says which kind of book is due next |
| A JATSI book in work or published | `book.json` `"collection": "jatsi"` (goes into the book JSON; the site labels the book from it) |
| The reader's explanation | the site page `japan-as-they-saw-it.html` (built from the two data files), the home page, `site/about.md` |
| Consistency of all this | `tools/ledger.py check`, run by the tests |

## The pace

`jatsi_policy`: `{"since": "2026-11-20", "others_before": 6, "others_per_jatsi": 2}`. Counting only books
started (in progress or published) since the policy began, a JATSI book is due whenever the other books started
number at least twice the JATSI books started: JATSI, other, other, JATSI, … — one book in three. (My reading of
"one JATSI book per every three books added"; if Tom meant one after every three others, set `others_per_jatsi`
to 3. Asked in `preferences.md`.) It is a pace, not a lock: when the JATSI book that is due cannot be started
(a scan problem, a tool not ready), take another book and let the count catch up.

## Which rules apply to a JATSI book (`selection.md` has the rules)

| Rule | For a JATSI book |
|---|---|
| 1. a complete, good scan at IA | **Required.** Not necessarily the scan JATSI links: look for a better one of the same edition (many JATSI links are Google or Digital Library of India scans). The edition JATSI lists is the one to transcribe when a good scan of it exists; otherwise the first edition, or the best-scanned one, said in `edition_statement` |
| 2. no digital text elsewhere | Not required. Checked and recorded. Books without one come first; the 44 with a Project Gutenberg text (`gutenberg` in `jatsi.json`) come last (assumed; asked) |
| 3. not reprinted after 1914 | Not required. Checked and recorded |
| 4. a first-person account of the author's own travel | Not required, but it sets the order: `kind` `narrative` first, then `mixed`, then `other` (histories, compilations, guidebooks, reference works: years away, and Tom will be asked again before the first of them) |
| 5. every author dead more than 70 years | **Required** (it is about copyright, not taste). `hold` in `jatsi.json` marks the ones known to fail, with the year they become free |

The queue row's `eligibility` says, for each rule, met or not and what was searched, exactly as for other books,
and begins "JATSI <n>." so that nobody takes an unmet rule 2 or 3 for an oversight. Nothing on the site may say
of a JATSI book that it has no other edition unless that was checked and is true.

## Choosing the next JATSI books

Keep at least four JATSI rows `queued` (`ledger.py` says when there are fewer). To add more: take `narrative`
entries without `gutenberg` or `hold` from `data/jatsi.json`, vet them by the `select-book` procedure (all five
checks, the scan looked at, twenty pages read), and prefer, in this order: books that meet all five rules; books
wholly or mostly about Japan (the others are round-the-world books with a Japan chapter — still eligible, and
the whole book is transcribed, not only the Japan part: assumed, asked); a spread over the decades 1855–1912 and
over kinds of writer (naval officers, diplomats, teachers, missionaries, tourists, residents); single volumes
within the tools' reach. Correct `kind` in `jatsi.json` when reading shows the one-line summary misled.
A JATSI book that fails rule 1 or 5 gets a queue row `rejected` (or the `hold`), like any other.

Two entries are the same work twice: Oliphant's *Elgin's Mission* (n 13 British edition in two volumes, n 16
American edition in one); Dilke's "English Influence in Japan" (n 42) is a chapter of *Greater Britain* (n 25).
Do each work once and say on the queue row which entries it covers.

## What these books bring that the others have not

- **Japanese words and names in the author's romanization** (Yedo, Tôkiyô, Kiôto, Hakodadi, jinrikisha, daimio):
  exactly the place where models write the familiar form. Macrons and circumflexes as printed. Every judge spot
  and audit candidate on such a word gets a crop. `regions` in `book.json` uses the modern names.
- **Japanese script** (kanji, kana) printed in the text or on plates: untested (`workflow.md` §"Not yet solved").
  Look for it at the scan check; a book with more than a few characters waits until a sample has been tried.
- **Many halftone photographs** in the books after about 1895, often with captions set among the text.
- **Editions**: JATSI sometimes lists a late edition (the seventh of *The Mikado's Empire*) or a reissue; the year
  in `jatsi.json` is that of the copy listed.

## Log

| Date | What |
|---|---|
| 2026-11-20 | List taken from the Sources page (247 entries); IA metadata and a Gutenberg catalogue match for all; `kind` assigned from the one-line summaries (narrative 105, mixed 39, other 103); 26 narratives vetted by Opus subagents; the first rows queued (below, in `data/queue.json`). Session run on Fable by Tom's choice. |
