#!/bin/bash
# Regression tests for the tools: a few seconds, no model calls. See tests/test_tools.py for the rules.
cd "$(dirname "$0")/.." && exec python3 -W ignore::ResourceWarning -m unittest discover -s tests "$@"
