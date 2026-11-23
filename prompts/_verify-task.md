
## Your task: proofread a draft against the page image

Below, inside `<draft>` tags, is a transcription of this page in the page markup described above. It is mostly right. Compare it against the page image word by word and letter by letter — body text, proper names, numbers, punctuation, italics and small capitals, headings, paragraph breaks, the `[[cont]]` marker, footnotes and their marks, missing or repeated lines, running heads or signature marks left in — and report ONLY what must change. The image is the sole authority. The draft reads fluently even where it is wrong, so do not read it for sense: check each word against the shapes on the scan, and look hardest at words that look modern or familiar. Do not "improve" the author's wording or spelling, and do not report differences of spacing that follow the rules above.

Reply with a corrections list, one JSON object per line and nothing else:

{"find": "exact text copied from the draft", "replace": "corrected text"}

- `find` must be copied exactly from the draft and must occur exactly once in it: include just enough neighbouring characters (usually 5–15) to make it unique, no more.
- To delete text use an empty `replace`; to insert, put the neighbouring text in `find` and the same text plus the insertion in `replace`.
- If the draft is entirely correct, reply with the single word NONE.
