# template-plugin marketplace

A minimal Claude Code plugin marketplace distributing two plugins, each bundling a Python MCP server:

- **csv-demo** — one tool, `describe_csv_file`: statistical summary of a CSV file (documented below)
- **txt-demo** — one tool, `describe_text_file`: line/word/char counts; demonstrates importing shared code (`shared/operations.py`) via a symlink that gets dereferenced on install

## What it does

Exposes a single MCP tool that reads a CSV file with `case_id` and `usd_amount` columns and returns a statistical summary.

**Tool name:** `mcp__plugin_csv-demo_csv-tools__describe_csv_file`

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `string` | Absolute path to the CSV file |

**Output (success):**

```json
{
  "row_count": 3,
  "columns": ["case_id", "usd_amount"],
  "case_ids": ["C001", "C002", "C003"],
  "usd_amount": {
    "total": 350.75,
    "min": 50.25,
    "max": 200.50,
    "mean": 116.92
  }
}
```

**Output (error):** `{ "error": "<reason>" }` — file not found, empty file, missing columns, or non-numeric `usd_amount`.

## Installation

```shell
/plugin marketplace add barbiquilmes/template-plugin
/plugin install csv-demo@template-plugin
/plugin install txt-demo@template-plugin
```

Then run `/reload-plugins` and the MCP server will connect. No restart needed.

**Requirements:** [`uv`](https://docs.astral.sh/uv/) must be on your PATH. Dependencies are resolved automatically by `uv run` on first use.

## Usage

```
Describe my CSV file at /path/to/your/file.csv
```

Claude will call the MCP tool automatically.

## How Claude Code manages plugin files

See [PLUGIN-FILES.md](PLUGIN-FILES.md) for the full lifecycle: what each `/plugin` command creates on disk, how `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA` behave, and what happens on update and uninstall.

## Local development

```bash
# Load one plugin without installing (point at the plugin dir, not the marketplace root)
claude --plugin-dir ./plugins/csv-demo

# Reload after changing .mcp.json or hooks (SKILL.md changes are live instantly)
/reload-plugins
```

## Testing

Tests call `describe_csv_file` directly as a plain Python function — no plugin loaded, no MCP server running. The `conftest.py` stubs out the `mcp` package so importing `server.py` works without the plugin venv.

```bash
cd plugins/csv-demo && python3 -m pytest tests/ -v
```

## Project structure

```
template-plugin/              # marketplace root — not itself a plugin
├── .claude-plugin/
│   └── marketplace.json      # Catalog: lists csv-demo and txt-demo
├── shared/
│   └── operations.py         # Shared code, reachable from plugins only via symlinks
└── plugins/
    ├── csv-demo/
    │   ├── .claude-plugin/plugin.json
    │   ├── .mcp.json         # Declares csv-tools stdio server
    │   ├── src/server.py     # FastMCP server — describe_csv_file
    │   ├── hooks/hooks.json  # No active hooks (uv run handles deps automatically)
    │   └── tests/            # conftest.py stubs mcp; pytest tests for describe_csv_file
    └── txt-demo/
        ├── .claude-plugin/plugin.json
        ├── .mcp.json         # Declares txt-tools stdio server
        ├── src/server.py     # FastMCP server — describe_text_file
        └── shared → ../../shared  # Symlink; dereferenced (content copied) on install
```
