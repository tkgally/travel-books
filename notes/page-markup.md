# Page markup

One UTF-8 text file per IA leaf, `pNNNN.txt` (NNNN = the number in the scan's image file names). Written by the
models (`prompts/_format.md` is the wording they get), edited by the session, read by `tools/compile_book.py`.

| Markup | Meaning |
|---|---|
| `[[page N]]` (line 1) | printed page number as printed; `?` if none |
| `[[blank]]` | blank page |
| a line of text | one paragraph (paragraphs are separated by a blank line; a paragraph is never broken over lines) |
| `[[cont]]` at the start of the page's first paragraph | it continues the previous page's last paragraph (joined with a space; a page-final hyphen is removed unless the page is in `keep_hyphens`; no space at a dash) |
| `# ` / `## ` / `### ` | main division (starts a new division, file and contents entry) / section / subsection |
| `[[subtitle]] text` | chapter title or summary printed under the chapter number; joined to the contents entry if short |
| `<i> <b> <sc> <sup> <sub>` | italic, bold, small capitals (typed in lower case), superscript, subscript; balanced within the paragraph, not nested in themselves |
| `[[right]] text`, `[[center]] text` | a short line set flush right / centred |
| `[[break]]` | a break between paragraphs marked by space or an ornament |
| `[[image: description]]` | illustration; file `images/pNNNN-k.jpg` (k-th image on the leaf); the description is the alt text |
| `[[caption]] text` | printed caption of the image just before |
| `[[fnref *]]` / `[[fn *]] text` | note reference / note (at the end of the page file); the k-th reference with a mark pairs with the k-th note with that mark in the division |
| `[[fn cont]] text` | continuation of the previous page's last note |
| `<blockquote>` … `</blockquote>` (own lines) | set-off prose, one paragraph per line; `[[right]]`/`[[center]]` allowed at line start |
| `<verse>` … `</verse>` (own lines) | verse, one printed line per line, an empty line between stanzas |
| `[[cont]]` at the start of the first line inside a blockquote or verse at the top of a page | it continues the previous page's quotation (prose is joined mid-paragraph unless the previous line ended a sentence; verse continues as a new line of the same stanza) |
| pipe rows `| a | b |` | table |
| `<pref>34</pref>`, `<pref to="34">text</pref>` | the book's own reference to its page 34: becomes a link when page 34 is in the reading editions |
| `[[corr printed|corrected]]` | a printer's error corrected by us (`style.md`) |
| `〓` | illegible character |

Editing by hand: never "fix" the author's spelling; only fix transcription and markup. Straight quotes typed
by hand are curled by the compiler (`'tis`-type elisions are recognised from a list in `tools/inline.py`: for
any other word-initial apostrophe type `’`).
