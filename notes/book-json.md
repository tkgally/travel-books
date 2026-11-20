# book.json, source.json, log.md

## book.json (in `wip/<slug>/` then `books/<slug>/`)

```
{
 "id": "flying-leaves-pfeiffer",        directory name: short title words + author surname, lower case, hyphens
 "version": 1,                          +1 for every published change
 "date": "2026-11-25",                  date of this version (also the EPUB's modification date)
 "title": "…", "subtitle": "…",         as on the title page, capitals reduced to title case
 "short_title": "…",                    for lists and breadcrumbs
 "authors": [{"name": "Emily Pfeiffer", "sort": "Pfeiffer, Emily", "born": 1827, "died": 1890}],
                                        an editor whose work is in the book: same keys + "role": "editor" (shown as "edited by")
 "place": "London", "publisher": "Field & Tuer", "year": 1885,
 "edition_statement": "First edition",  what was transcribed (edition, printing, volume)
 "regions": ["Greece", "Turkey", "United States"],     modern names, most specific useful level
 "period": "1882–84",                   when the journey took place
 "subjects": ["…"],                     optional, plain terms
 "summary": "…",                        60–150 words, style.md §Site text (a string or a list of paragraphs)
 "source": {"ia_identifier": "…", "contributor": "University of California Libraries",
            "hidden_leaves": [0, 321]}, from prep_pages.py's leaves.json: leaves IA's viewer does not show
            a work in several IA items (volumes) adds "items": [{"ia_identifier": "…", "first_leaf": "p1000",
            "hidden_leaves": […], "label": "Volume I"}, …]: that item's IA leaf k is page file p1000+k (scan links,
            preflight leaves; the book page links and embeds every item, by its label)
 "leaf_order": [["p1469", "p1470", "p1467", "p1468"]],  leaves bound out of order in the scanned copy, read in this order
 "omitted_from_reading": "The half-title, printed contents, index and advertisements are in the JSON only.",
 "notes_on_text": ["…"],                anything a reader of the text should know (errata slip applied, a damaged page …)
 "history": [{"version": 1, "date": "2026-11-25", "note": "First publication."}],
 "audit": {"version": 1, "date": "…", "pages": 6, "recall": "30/30", "real_errors": 0, "fixed": 0},
 "divisions": [ … ],                    exceptions to "each # heading is a chapter in the reading editions"
 "toc": {"subtitles": "all"},           contents entries with every chapter summary in full (default: only those of 80 characters or fewer)
 "toc_entries": [{"at": "p0043", "starts": "15th.—", "title": "15–30 June: London; Oxford and Windsor"}],
                                        entries inside a division: the block starting on page `at` whose plain text
                                        starts with `starts`; "editor": false for a title taken from the printed contents
 "frontispiece": "p0010-1",               image moved from the front matter to the start of the first reading division
 "keep_hyphens": ["p0034"],             pages whose join with the previous page keeps the hyphen
 "waivers": [{"check": "…", "match": "…", "why": "…"}],
 "css_extra": ""                        rarely
}
```
`divisions` entries: `{"at": "p0013", "kind": "contents"}`; optional `title`, `toc_title` (the contents entry, when
it should differ from the title), `reading` (true/false), `n` (the n-th division starting on that page). Kinds: front, titlepage, dedication, preface, contents, illustrations,
introduction, part, chapter, appendix, notes, glossary, index, errata, advertisements, back. Left out of the
reading editions by default: front, titlepage, contents, illustrations, index, errata, advertisements, back.
A `#` division with headings only (and a `[[subtitle]]`) becomes a `part` and the chapters after it nest under it.
How the contents are decided for a book: `workflow.md` stage 4 "Contents".

## source.json

`{"ia_identifier", "drive_folder_id", "prep": {"height": 1800, "quality": 72}, "parts": [{"name", "sha256",
"bytes", "files", "drive_id"}]}` — written by `tools/drive_cache.py`; `ia_identifier` and `drive_folder_id` by hand.

## log.md template

```
# <Title> — <Author> (<year>)

IA: <identifier> (<contributor>; <n> leaves). Other scans looked at: …
Eligibility: re-checked <date>: …

## Status
Stage reached: …            Next step (exact command): …           Half-finished: …

## Page map
p0000 colour card · p0001 cover · p0005 title · p0009–p0012 contents · p0013 = printed 1 (offset 12) · …
Plates: p0004 (frontispiece), … Scan check: all sheets looked at <date>; full size: p…, p…; problems: none / …

## Decisions
- … (mark "assumed" what Tom has not confirmed)

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
```
