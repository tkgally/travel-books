## Output format ("page markup")

Output ONLY the transcription of this one page, in the plain-text markup below. No commentary, no code fences.

- Line 1 is always `[[page N]]`, where N is the page number printed on the page (arabic or roman, as printed; `[[page ?]]` if none is printed).
- Then the page's content, paragraphs separated by one blank line. Each paragraph is ONE line: join its printed lines.
- If the page's first paragraph continues a paragraph begun on the previous page (it does not start with a paragraph indent), start it with `[[cont]]`.
- Headings: `# ` for the title of a chapter or other main division (`# CHAPTER IV.`, `# PREFACE.`, `# APPENDIX.`); `## ` for a section heading inside a chapter; `### ` for a smaller one. Type the heading as printed.
- A chapter title or summary of contents printed under the chapter number (`Departure from Cairo—The Nile—A Sand-storm`) goes on the next line as `[[subtitle]] text`.
- A short line set flush right (a signature, a place and date closing a letter) starts with `[[right]]`; a short centred line that is not a heading (an inscription, `THE END`) starts with `[[center]]`.
- A space or ornament printed between paragraphs to mark a break in the narrative: a line with only `[[break]]`.
- Illustrations, maps, plates, diagrams: `[[image: a few words describing it]]` on its own line where it occurs; do not transcribe lettering that is inside the picture. A printed caption goes on the next line as `[[caption]] caption text`.
- Footnotes printed at the foot of the page: one per line at the end, `[[fn *]] note text`, with the mark as printed (`*`, `†`, `1`). Mark the reference in the text as `[[fnref *]]`. A note continued from the previous page: `[[fn cont]] text`.
- Prose set off from the text (a quoted letter, an extract in smaller type): a line `<blockquote>`, its paragraphs one per line, a line `</blockquote>`.
- Verse: a line `<verse>`, each printed line of verse on its own line, an empty line between stanzas, a line `</verse>`.
- If a quotation or verse continues from the previous page, put `[[cont]]` at the start of its first line.
- Tables: simple pipe tables, one row per line (`| a | b |`).
- A reference to another page OF THIS SAME BOOK (`see p. 34`): wrap just the number, `p. <pref>34</pref>`. Not for pages of other books.
- A blank page is `[[page ?]]` followed by `[[blank]]`. A page with only a picture has the `[[page ?]]` line and the `[[image: …]]` line.
- If a character is truly illegible write `〓`.
