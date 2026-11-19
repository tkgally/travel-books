You are transcribing one scanned page of a travel book printed in English before 1914, for an accurate public edition.

## Reading rules

- Transcribe EXACTLY the words, spelling, capitals and punctuation marks that are printed. Do not correct, modernize, regularize, translate, summarize or omit anything: old and inconsistent spellings (`shew`, `to-day`, `connexion`, `Mahomet`, `Pekin`), odd place-names and apparent misprints all stay as printed. Read proper names and foreign words letter by letter; do not replace them with the form you know.
- Spacing is the one thing that is modernized: no space before `;` `:` `!` `?` or inside quotation marks, even where the print has one; contractions printed with a space are closed up (`do n't` → `don't`); dashes are closed up to the words on both sides.
- Rejoin words hyphenated across line ends (`inter-` / `national` → `international`), but keep a hyphen that belongs to the word (`to-` / `day` → `to-day`, `twenty-` / `third` → `twenty-third`). If the LAST word on the page is broken by a hyphen, keep the trailing hyphen exactly as printed.
- Typographic characters as printed: curly quotes “ ” ‘ ’, em dash —, accented letters, £, ½, °. Ligatures as plain letters (fi, fl, æ and œ stay as æ, œ). Long s (ſ) is written s.
- Italics: mark every italic run with `<i>…</i>` (ship names, foreign words, titles, emphasis), with punctuation inside the tag only if it too is italic.
- Small capitals: wrap in `<sc>…</sc>` and type them in lower case, with a capital only where the print has a visibly taller full capital (`<sc>Constantinople</sc>`, a chapter's opening words `T<sc>he</sc>`). Text in full-size capitals stays as plain capitals, without the tag.
- OMIT: running heads and feet, the page number, printers' signature marks at the foot of the page (`B 2`, `VOL. I. C`), catchwords, library stamps and pencil marks.

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

## Your task: proofread a draft against the page image

Below, inside `<draft>` tags, is a transcription of this page in the page markup described above. It is mostly right. Compare it against the page image word by word and letter by letter — body text, proper names, numbers, punctuation, italics and small capitals, headings, paragraph breaks, the `[[cont]]` marker, footnotes and their marks, missing or repeated lines, running heads or signature marks left in — and report ONLY what must change. The image is the sole authority. The draft reads fluently even where it is wrong, so do not read it for sense: check each word against the shapes on the scan, and look hardest at words that look modern or familiar. Do not "improve" the author's wording or spelling, and do not report differences of spacing that follow the rules above.

Reply with a corrections list, one JSON object per line and nothing else:

{"find": "exact text copied from the draft", "replace": "corrected text"}

- `find` must be copied exactly from the draft and must occur exactly once in it: include just enough neighbouring characters (usually 5–15) to make it unique, no more.
- To delete text use an empty `replace`; to insert, put the neighbouring text in `find` and the same text plus the insertion in `replace`.
- If the draft is entirely correct, reply with the single word NONE.
