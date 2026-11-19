#!/bin/bash
# Regenerate the prompts given to models from their parts. Run after editing prompts/_*.md.
cd "$(dirname "$0")/../prompts" || exit 1
{ cat _rules.md; echo; cat _format.md; } > transcribe.md
{ cat _rules.md; echo; cat _format.md; cat _verify-task.md; } > verify.md
echo "wrote prompts/transcribe.md prompts/verify.md"
