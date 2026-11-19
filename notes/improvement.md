# How the method is improved

The aim is that each book is done a little better than the last and that nothing is learned twice.

## In every session

- A miss (an error that got further than it should) is turned, in that session, into a preflight check
  (starting in `observe`), a test, or a line in `lessons.md` — in that order of preference.
- A false alarm from a check is recorded in `metrics.md` §"Preflight checks"; the check is fixed, with a test,
  as `workflow.md` §"When a check is wrong" says (the session that fixes it does not publish the book it blocked).
- Anything that stopped or ended a session (a refusal, a blocked action, a hang) is written where the next
  session will meet it: a tool message, `RESUME.md` §3, or CLAUDE.md if it is a rule.
- Each published version gets a row in `metrics.md`.

## Review sessions (every fifth published book, or when the numbers say so)

No new book. Read `metrics.md`, `errata.md`, `lessons.md` and the last five book logs, then:

1. **Where do errors come from?** Tabulate errata and audit finds by kind (misread letter, modernized
   spelling, punctuation, markup, structure, metadata) and by the stage that should have caught them. The
   largest class gets a change: a prompt line, a check, a different pipeline for that kind of book.
2. **Is each stage earning its cost?** Spots judged, how often the judge overturned the verifier, how often
   the scan overturned the judge, audit recall, dollars per page. A stage that changes nothing over five
   books is tested without (on a sample, with `score.py`) before it is dropped; a stage that is often wrong
   gets a second look at its prompt.
3. **Checks:** promote `observe` checks whose alarms were mostly real; fix or drop the noisy ones.
4. **Notes:** prune `lessons.md` (delete what tools enforce, merge duplicates); bring the skills and
   `workflow.md` to the current procedure; make sure `site/about.md` still describes what is done.
5. **Earlier books:** does any published book now differ visibly from the current style, or would the
   current pipeline fix a significant number of errors in it? If so, add a row to the queue to redo it.
6. **Site:** open the live site on a narrow and a wide screen; check the landing page, one book page, one
   chapter; run an accessibility pass (headings in order, link text, contrast, keyboard focus).
7. **This file:** is the review itself finding things? If two reviews in a row change nothing, lengthen the
   interval; if errata arrive faster than reviews, shorten it. Record what the review changed below.

Benchmarks before changing models or pipeline: 12–16 pages of a published book whose text has been through
audit and errata (the best ground truth available), `tools/score.py`, results in `metrics.md`.

## Review log

| Date | Books covered | What changed |
|---|---|---|
| 2026-11-19 | the first five books (Rajah, Sketches Awheel, Flying Leaves, South by West, Corona and Coronet; 1,730 drafted pages) | **Errors:** 3 errata, all contents (none of text); audits 0 real errors in 38 pages + 8 fallback pages, recall 30/30 every time (so the audit bounds the error rate only loosely). Judge 146 spots: draft 99, Sonnet 46, structural 1; scan overturned the judge once (Rajah p0170, a name). **Stages:** all kept: the Sonnet pass (~30% of the cost) supplied 46 accepted changes, among them the only name error caught; the judge costs ~2%. Claude ≈ $0.10 a page for every book ($166 for five). **Checks:** `hyphen-joins` read 122 items for 6 real keeps → now leaves out joins the book itself settles (27 items left, all 6 keeps among them); `joins` 37 alarms, 0 real (all flush-left continuations): kept in observe, drop the "after a closed sentence" half at the next review if still none is real; `contents` 7, all explained; `folios`, `quote-balance` (1, waived as printed) quiet. **Site:** narrow and wide, headings in order, alt text, focus outline, no sideways scroll: fine; a short chapter title under a centred heading looked like a stray indented paragraph → centred (HTML, EPUB, ODT). **Earlier books:** none needs redoing (all from the current pipeline; the deploy rebuilds their editions). **Next:** marginal notes before Staunton (workflow "Not yet solved"). Next review after five more books. |
| 2026-11-19 | the first four routine sessions (Tom asked for a diagnosis) | Causes found: output-filter refusals with no working route, and a session ended by typing a refused page; finished books held by preflight false alarms that the rules forbade fixing; an eligibility question left until a book was done. Changes: `ocr_fallback.py`; conservation follows moved images and lists differences in long texts; the checks rule and RESUME §3 rewritten; Tom's answers committed before acting. |
| 2026-11-19 | — (set-up) | Pipeline, checks and notes taken over from pdf-to-epub's English workflow and rebuilt around a book JSON; first calibration in `metrics.md`. |
