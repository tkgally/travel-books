# My Last Cruise — A. W. Habersham (1857)

IA: mylastcruiseorwh00habe (University of California; 590 leaves, 400 ppi). Leaf for pp. 125–126 from mylastcruiseorwh01habe (Library of Congress copy of the same edition, viewer pages n144–n145) as p0148a, p0148b.
Eligibility: re-checked 2026-11-28: web search finds catalogue records only (Nichibun, Harvard); JATSI 7.

## Status
Stage reached: (c) audit 30/30; preflight lacks only the audit before it was recorded; rendered look by a subagent under way.
Next step: preflight PASS, `publish.py my-last-cruise-habersham`.

## Page map
p0001 cover · p0002–p0007 endpapers, blanks · p0008 frontispiece “Women admiring a Watch. In Japan.” · p0009–p0010 tissue (hidden) · p0011 engraved title (vignette “Camoens Grot.”) · p0012 blank · p0013 printed title · p0014 copyright · p0015 dedication · p0017–p0018 Preface (5–6) · p0019–p0023 Contents (7–11) · p0025 Chapter I = printed 13 (offset 12, +2 after each plate) · chapters I p0025, II p0037, III p0051, IV p0068, V p0088, VI p0106, VII p0131, VIII p0149, IX p0167, X p0185, XI p0208, XII p0241, XIII p0261, XIV p0281, XV p0316, XVI p0345, XVII p0371, XVIII p0401, XIX p0430, XX p0453, XXI p0468, XXII p0488, XXIII p0513, XXIV p0549, Conclusion p0561 · p0573 = p. 507, The End · p0575–p0578 Lippincott advertisements (4 pp.) · p0579–p0584 blanks, endpapers, back cover.
**The UC copy lacks the leaf pp. 125–126** (p0148 = p. 124 ends “I only know the”; p0149 = p. 127): taken from the LoC copy (n144 = p. 125 “above, which I learned …”, n145 = p. 126, looked at by the session).
Plates (29 leaves with blank versos; S = sideways): p0008, p0011 (engraved title), p0033 S, p0115 S, p0125 S, p0137 S, p0141, p0145, p0155 S, p0181 S, p0201 S, p0211, p0223, p0225, p0229, p0239, p0251 S, p0291 (tissue), p0313 S, p0325 S, p0339, p0347 S, p0365, p0383 S, p0391, p0441 S, p0485 S, p0503 S, p0543 S.
Scan check: all 15 sheets, edge strips of 16 leaves, page numbers (Opus subagent, 2026-11-28).
Notes: chapter summaries in small capitals; first word in small capitals; journal extracts in quotation marks; small-type extracts (p0311, p0360–p0363); “* * *” breaks; a footnote p0307; verse p0056; a two-column list of officers p0134; period romanizations (Si-mo-da, Ha-ko-da-di, Loo-Choo) to keep.

## Decisions
- The missing leaf taken from the LoC copy (workflow §1.4); `source.extra_leaves`; said in `notes_on_text`.
- Divisions: the engraved title (before the printed title), the printed contents, the book's title above Chapter I and the publisher's advertisements in the JSON only; the frontispiece moved to the title page; chapter summaries in full in the contents (`toc.subtitles: all`).
- Cover: the printed title page (the cloth cover has no readable title).
- The draft read a blank verso (p0574) from the show-through of p. 507: set `[[blank]]` before the corrections pass.
- Summaries printed in capitals made one title-case form; seven printer's errors marked (aud, precations, sufficent, sufficently, two opening quotation marks, a stray hyphen at a page end); `keep_hyphens` for six compounds.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-28 | Opus | 573 | 37.78 | no refusals; one blank verso filled from show-through (set blank) |
| Corrections | 2026-11-28 | Sonnet | 573 | 18.66 | 23 changes; a blank (p0224) filled with show-through, refused; a `[[cont]]` proposal not applied |
| Judge | 2026-11-28 | Opus | 10 spots | 0.41 | draft 8, verified 2; on crops: Selio kept (the book's spelling), a closing quotation mark restored (p0530), aud marked |
| Spot-read | 2026-11-28 | Opus subagent | front matter, openings, captions, lists | — | 32 edits: title page lines, summaries and captions in one title case, leaders in the contents, 6 printed errors marked |
| Audit | 2026-11-28 | Opus | 6 | 0.34 | 30/30 planted errors found; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
