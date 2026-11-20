# Sessions

One row per session, added at the session's first commit (start time, end empty) and completed at its close
(`RESUME.md` §4 and §5). `python3 tools/session_meter.py --row` prints the first cells. Times are UTC. "Context"
is the tokens in the context window at the close and their share of the window; "Sum." is how many times the
conversation was summarized (compacted). In "Work", give the context share after each book, so that the cost
of a book in context can be read off. Tom sets the interval of the routine from the hours; reviews
(`improvement.md`) set the table in `RESUME.md` §3 from the context figures.

| Start | End | Hours | Context at the close | Sum. | Model | Work (context share after each piece) | Cost, API-equivalent |
|---|---|---|---|---|---|---|---|
