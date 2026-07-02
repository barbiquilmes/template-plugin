#!/usr/bin/env python3
"""Print line/word/char counts of a UTF-8 text file as JSON.

Uses count_words from shared/operations.py at the marketplace root — the
same helper the txt-demo MCP server uses — reached through the plugin's
`shared` symlink (dereferenced into a real directory on install).

Runs on plain python3 with no third-party dependencies: skills need no
server process and no venv, in contrast to the MCP approach.
"""

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT))

from shared.operations import count_words


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: describe_txt.py <path>"}))
        return 1
    p = Path(sys.argv[1])
    if not p.is_file():
        print(json.dumps({"error": f"file not found: {p}"}))
        return 1
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(json.dumps({"error": f"not a UTF-8 text file: {p}"}))
        return 1
    print(json.dumps(count_words(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
