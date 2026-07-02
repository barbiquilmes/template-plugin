---
name: describe-txt
description: This skill should be used when the user asks to "describe a text file", "count lines in a txt file", "count words in a text file", or wants line/word/character statistics for a plain-text (.txt) file.
---

# Describe a text file

To describe a UTF-8 text file, run the bundled script with the file path as its only argument:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/describe-txt/scripts/describe_txt.py" /path/to/file.txt
```

The script prints one JSON object:

- Success: `{"line_count": N, "word_count": N, "char_count": N}`
- Failure: `{"error": "<reason>"}` (file not found, not UTF-8, bad usage)

Report the counts to the user in a short sentence. On error, relay the reason.

The script needs only `python3` — no venv, no third-party packages. It imports
`count_words` from `shared/operations.py`, the same helper the txt-demo MCP
server uses, so both plugins stay consistent.
