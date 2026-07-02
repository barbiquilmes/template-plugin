# csv-demo plugin

A minimal Claude Code plugin that bundles a Python MCP server with one tool: `describe_csv_file`.

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
```

Then run `/reload-plugins` and the MCP server will connect. No restart needed.

**Requirements:** [`uv`](https://docs.astral.sh/uv/) must be on your PATH. Dependencies are resolved automatically by `uv run` on first use.

## Usage

```
Describe my CSV file at /path/to/your/file.csv
```

Claude will call the MCP tool automatically.

## Local development

```bash
# Load without installing
claude --plugin-dir ./template-plugin

# Reload after changing .mcp.json or hooks (SKILL.md changes are live instantly)
/reload-plugins
```

## Testing

Tests call `describe_csv_file` directly as a plain Python function — no plugin loaded, no MCP server running. The `conftest.py` stubs out the `mcp` package so importing `server.py` works without the plugin venv.

```bash
python3 -m pytest tests/ -v
```

## Project structure

```
template-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (name: csv-demo)
├── src/
│   └── server.py         # FastMCP server — defines describe_csv_file
├── hooks/
│   └── hooks.json        # No active hooks (uv run handles deps automatically)
├── tests/
│   ├── conftest.py       # Stubs mcp so tests run without the plugin venv
│   └── test_server.py    # pytest tests for describe_csv_file
└── .mcp.json             # Declares csv-tools stdio server
```
