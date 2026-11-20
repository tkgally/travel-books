# Sessions

One row per session, added at the session's first commit (start time, end empty) and completed at its close
(`RESUME.md` §4 and §5). `python3 tools/session_meter.py --row` prints the first cells. Times are UTC. "Context"
is the tokens in the context window at the close and their share of the window; "Sum." is how many times the
conversation was summarized (compacted). In "Work", give the context share after each book, so that the cost
of a book in context can be read off. Tom sets the interval of the routine from the hours; reviews
(`improvement.md`) set the table in `RESUME.md` §3 from the context figures.

| Start | End | Hours | Context at the close | Sum. | Model | Work (context share after each piece) | Cost, API-equivalent |
|---|---|---|---|---|---|---|---|
| 2026-11-20 06:57 | 07:55 | 0.97 | 431,844 (43%) | 0 | Opus 5.5 | Review after ten books (check `joins` half dropped; new check `image-splits`; *South by West* v2, *Journal of a Residence* v2; review row) — 17%. *A Woman's Winter in Africa* rejected at the scan check (slip over two leaves). Nine books vetted and queued by three subagents. *Via Rhodesia* published (450 pp., 148 pictures) — 37%. *W.S.W.* published (168 pp.) — 43%; closed by the table (40–60%: no new book). Heavy use of Opus subagents for scan checks, crops and vetting kept images out of the context. | $63.09 in model runs (Via Rhodesia 47.13, W.S.W. 15.96); subagents not metered separately; OpenRouter $0 |
| 2026-11-20 08:08 | 09:17 | 1.15 | 425,000 (42%) | 0 | Opus 5.5 | *A Cruise in the U.S. Steam Frigate Mississippi* (Gragg, JATSI, 76 pp.) published — 21%. *A Journey through the Caucasus* (Mounsey, 364 pp.) published — 28%. *The West Coast of Africa* (Dyer, 202 pp.) published — 36%. Review after fifteen books (`image-splits` enforced; new check `site-text`; *Corona* v3, *Rajah* v5, *Caucasus* v2 for straight apostrophes in book.json) — 37%. *A Jaunt in Japan* (Jackson, JATSI, 176 pp.) published — 42%; closed by the table. About 10% of the context per book: every look at images (scan checks, spot-reads, rendered looks, judge crops beyond a few) went to Opus subagents, Drive uploads to Haiku subagents; corrections passes started on the drafted half while the draft ran. | $79.68 in model runs (Cruise 11.08, Caucasus 33.98, West Coast 18.97, Jaunt 15.65); subagents not metered separately; OpenRouter $0 |
