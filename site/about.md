# About

This site publishes travel books from the past in forms that are easy to read and to use: web pages, EPUB, ODT and JSON. The project began in November 2026 and is run by Tom Gally. The books are chosen, transcribed and checked by Claude, an AI model made by Anthropic.

## Which books

For now a book is included only if all of these are true:

- It is a first-person, nonfiction account of the author's own travels, written in English and published before 1914.
- A complete, good scan of it is at the [Internet Archive](https://archive.org/).
- Its text is not available anywhere else on the Internet, apart from the Internet Archive's automatic text recognition and short excerpts.
- It has not been published in print since 1914, apart from short excerpts and print-on-demand copies of scans.

Among the books that qualify, the choice is Claude's. The aim is a varied set of readable books that are otherwise found only in libraries or as page scans.

These books were written between about one and four centuries ago. They contain opinions about peoples, religions, women, empire and animals that many readers now will find wrong or offensive. The texts are given as they were printed.

## How the texts are made

Each page of the scan is read by one Claude model and proofread against the page image by another. Where the two differ, a third reading decides, and uncertain places are checked against enlarged images of the print. Before a book is published, a set of automatic checks must pass, and a sample of pages is proofread again with deliberate errors added, to measure how many errors the proofreading finds.

No transcription is free of errors. If you find one, please [report it on GitHub](https://github.com/tkgally/travel-books/issues), giving the book and the page or a few words of the passage. Corrected versions are published as needed; each book's page lists its versions.

## The text

- The author's words, spelling, capital letters and punctuation are kept as printed, including old and inconsistent spellings.
- Spaces around punctuation follow modern practice.
- Words divided at the ends of lines are joined.
- Clear printer's errors are corrected. Each correction is listed on the book's page and recorded in the JSON with the printed reading.
- Illustrations and their captions are included. Footnotes are linked.
- The web pages, EPUB and ODT leave out some parts of the printed book, usually the printed table of contents, the index and the publisher's advertisements. The JSON has everything that was transcribed.

On the web pages you can show the page numbers of the printed book. Each number links to that page of the scan.

## Formats

- **Web pages**: one page for each chapter or other division.
- **EPUB**: for e-readers and reading apps.
- **ODT**: OpenDocument Text, for LibreOffice, Word and other word processors. All books use the same named styles.
- **JSON**: the complete transcription with its structure, page breaks and corrections. The other formats are built from it. See [the JSON format](json-format.html).

## Copyright

The books were published before 1914. The transcriptions, the markup, the text of this site and the software that builds it are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). You may copy, change and republish them without asking. The scans belong to the Internet Archive's collections and the libraries that made them; this site links to them and does not copy them, except for the illustrations.

## How the site is built

The source of every book, the tools and the working notes are in the [GitHub repository](https://github.com/tkgally/travel-books). The site uses no trackers, no cookies, and no fonts or scripts from other sites. The only outside content is the optional viewer of scanned pages on each book's page, which comes from the Internet Archive when you open it.
