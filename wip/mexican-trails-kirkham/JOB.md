# Job: mexican-trails-kirkham

Stanton Davis Kirkham, *Mexican Trails: A Record of Travel in Mexico, 1904–07, and a Glimpse at the Life of the
Mexican Indian* (New York and London: G. P. Putnam’s Sons, 1909). Scan: Internet Archive
`mexicantrailsrec00kirk_0` (Getty Research Institute), 382 leaves. The scan is complete and clean.

Follow `INSTRUCTIONS.md`. This file says what is particular to this book.

## What to transcribe

**Leaves p0008 to p0375**, every one, except p0011 and p0012 (tissue guards, which have no image here).
Blank leaves in the range get a page file with `[[page ?]]` and `[[blank]]`.

| Leaves | What | Printed pages |
|---|---|---|
| p0001 | front cover: not transcribed; the source of `images/cover.jpg` | |
| p0002–p0007 | endpapers: not transcribed | |
| p0008 | publisher’s list “By Stanton Davis Kirkham” (kind `front`) | |
| p0009 | blank | |
| p0010 | frontispiece | |
| p0013, p0014 | title page and its verso (kind `titlepage`) | |
| p0015 | dedication | |
| p0017–p0024 | Foreword (kind `preface`) | v–xii |
| p0025–p0026 | Contents | xiii–xiv |
| p0027–p0029 | Illustrations (the list) | xv–xvii |
| p0031–p0356 | Chapters I–XXV; “Mexican Trails” is printed again above Chapter I | 1–280 |
| p0357–p0369 | Index, two columns of small type | 281–293 |
| p0371–p0375 | publisher’s advertisements | |

Chapters begin on leaves p0031, p0045, p0059, p0074, p0083, p0098, p0115, p0128, p0146, p0173, p0179, p0187,
p0207, p0218, p0228, p0247, p0256, p0264, p0276, p0287, p0301, p0314, p0332, p0345, p0354. The plates are not
counted in the page numbers, so the difference between leaf number and printed page grows by two at each plate:
take the page number from each page itself.

## Pictures

24 photographs by the author, each a plate on its own leaf with a caption printed in type and a blank back:

p0010 (frontispiece), p0047, p0071, p0087, p0095, p0101, p0117, p0125, p0129, p0135, p0141, p0147, p0153, p0159,
p0165, p0169, p0191, p0197, p0203, p0233, p0273, p0291, p0311, p0341.

- Most are printed **sideways**, the caption reading up the right-hand side of the leaf: cut the photograph without
  its caption and turn it upright (`--rotate 270` for these; check each by looking at it). p0047, p0071 and p0311 are
  upright.
- They are photographs: no `--gray`.
- The page file of a plate leaf is `[[page ?]]`, the `[[image: …]]` line and the `[[caption]]` line. Type each caption
  from the plate itself, not from the list of illustrations (they differ in places).
- There are no maps, drawings or ornaments. The plain large initials at chapter openings are not pictures.
- `images/cover.jpg`: from leaf p0001 (dark cloth, the title stamped in a ruled box): the whole front board, upright.
- The full-size images of these leaves, and of p0001 and p0013, are in the `full-*.zip` files.

## Things to know

- **Spanish words** are frequent, mostly in italics, some with accents and some printed without (“señor”, “baño”,
  “Adios”, “Si! si!”). Type each as printed there: do not add or remove an accent to make it correct Spanish.
  The same for Mexican place-names (Tepoztlan, Xochicalco, “Guadalahara” in one chapter title).
- “Theologs” and “builded” are the author’s words.
- **Running heads** (“Mexican Trails” on left-hand pages, the chapter title on right-hand pages) and page numbers
  are left out, as the rules say.
- **Verse** in smaller type on printed pp. 86 and 88, perhaps elsewhere: `<verse>`.
- **Breaks** marked by a row of spaced dots (for example printed pp. 137 and 251): `[[break]]`.
- A placard quoted as separate lines (p. 146) and catechism questions and answers (pp. 265–266): type them as they
  are set (set-off lines as `<blockquote>`, one line each), and say in your notes what you did.
- No footnotes were seen; if you find one, use `[[fn *]]` as the rules say.
- **Contents and list of illustrations**: as the rules say for a contents page (entries as plain lines with the page
  number in `<pref>`).
- **Index**: one entry per line as its own paragraph, sub-entries as their own paragraphs, every page number in
  `<pref>`; do not make it a table. Read it enlarged: it is small type.
- Pencil marks and library labels are left out.

## book.json

Filled in already: title, author, publisher, year, source, `frontispiece`, `omitted_from_reading`. For you:
`divisions` (front p0008, titlepage p0013, dedication p0015, preface p0017, contents p0025, illustrations p0027,
index p0357, advertisements p0371, each with its `at`; add `"title"` where the page has no `# ` heading, as on the
title page and the dedication), `summary`, and `notes_on_text` if anything needs saying.
