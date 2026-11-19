"""Recognize the API's output-filter refusal, which is never retried (RESUME.md §3: "no retries, rephrasing
or chunking"). Used by the retry loops in ocr_claude.py, judge.py and audit_sample.py."""

MARK = "content filtering"


def is_refusal(err):
    """True if an error message (str or None) is the output filter's refusal."""
    return bool(err) and MARK in str(err).lower()
