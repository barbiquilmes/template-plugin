"""txt-demo MCP server: one tool that describes a UTF-8 text file.

Imports count_words from shared/operations.py, which lives at the
MARKETPLACE root, not inside this plugin. The import works because
plugins/txt-demo/shared is a symlink to ../../shared:
  - during local development the symlink resolves into the repo
  - on marketplace install Claude Code dereferences it, copying the
    shared content into this plugin's cache directory
"""

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT))

from shared.operations import count_words

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("txt-tools")


@mcp.tool()
def describe_text_file(path: str) -> str:
    """Return line, word, and character counts for a UTF-8 text file."""
    p = Path(path)
    if not p.is_file():
        return json.dumps({"error": f"file not found: {path}"})
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return json.dumps({"error": f"not a UTF-8 text file: {path}"})
    return json.dumps(count_words(text))


if __name__ == "__main__":
    mcp.run()
