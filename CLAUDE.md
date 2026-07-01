# Claude Code Plugin Template — with Bundled MCP Server
 
This project is a **teaching template** for building a Claude Code plugin that bundles a standalone Python MCP server.
The goal is to learn the minimal correct structure per Anthropic's official guidelines.
 
Docs: [MCP](https://code.claude.com/docs/en/mcp) · [Plugins](https://code.claude.com/docs/en/plugins) · [Complex plugins](https://code.claude.com/docs/en/plugins#develop-more-complex-plugins) · [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
 
---
 
## Project structure
 
```
template-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, description)
├── skills/
│   └── my-skill/
│       ├── SKILL.md         # Skill instructions + frontmatter
│       └── scripts/
│           └── run.py       # Script invoked by the skill
├── agents/
│   └── my-agent.md          # Subagent definition
├── hooks/
│   └── hooks.json           # Setup hook to bootstrap the Python venv
├── monitors/
│   └── monitors.json        # Background monitors (optional)
├── bin/                     # Executables added to PATH while plugin is enabled
├── settings.json            # Default settings applied when plugin is enabled
├── src/                     # MCP server source code (name is yours to choose)
│   └── server.py
├── .mcp.json                # Declares the MCP server; points to src/server.py
└── .lsp.json                # LSP server config (optional)
```
 
> ⚠️ Only `plugin.json` goes inside `.claude-plugin/`. Everything else lives at the plugin root.
> Reference: [Plugin structure overview](https://code.claude.com/docs/en/plugins#plugin-structure-overview)
 
---
 
## Key files explained
 
### `.claude-plugin/plugin.json`
The manifest. `name` is the only required field and controls the namespace for all components.
Skills become `/<name>:<skill-name>`, agents become `<name>:<agent-name>`, etc.
Reference: [Manifest schema](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)
 
### `skills/<skill-name>/SKILL.md`
Each skill is a folder with a `SKILL.md`. The folder name is the skill name.
Frontmatter must include `description` (how Claude decides when to invoke it).
Reference: [Skills](https://code.claude.com/docs/en/skills)
 
### `agents/<agent-name>.md`
Subagent definition with frontmatter: `name`, `description`, `model`, `maxTurns`, `tools`, etc.
Reference: [Subagents](https://code.claude.com/docs/en/sub-agents)
 
### `hooks/hooks.json`
Event handlers. The `Setup` event is where you bootstrap the Python venv into `$CLAUDE_PLUGIN_DATA`.
Reference: [Hooks](https://code.claude.com/docs/en/hooks)
 
### `src/server.py`
The actual MCP server code (stdio transport). Anthropic does not prescribe this folder name.
`$CLAUDE_PLUGIN_ROOT` always points here regardless of the name you choose.
Reference: [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server)
 
### `.mcp.json`
Declares how Claude Code starts the MCP server. Points `command` at the venv Python and `args` at `src/server.py`.
Plugin MCP servers start automatically when the plugin is enabled — no manual config needed by the user.
Reference: [MCP in plugins](https://code.claude.com/docs/en/mcp) · [Plugin MCP servers](https://code.claude.com/docs/en/plugins-reference#mcp-servers)
 
---
 
## The two critical env variables
 
| Variable | Survives plugin update? | Use for |
|---|---|---|
| `$CLAUDE_PLUGIN_ROOT` | No (changes on update) | Source code, config, scripts |
| `$CLAUDE_PLUGIN_DATA` | Yes | Python venv, caches, generated files |
 
> Never install Python dependencies into `$CLAUDE_PLUGIN_ROOT`.
> Reference: [Environment variables](https://code.claude.com/docs/en/plugins-reference#environment-variables)
 
---
 
## MCP tool naming convention

Tools exposed by a bundled MCP server are automatically prefixed by Claude Code:

```
mcp__plugin_<plugin-name>_<server-name>__<tool-name>
```

Example: plugin `csv-demo`, server `csv-tools`, tool `describe_csv_file` →
`mcp__plugin_csv-demo_csv-tools__describe_csv_file`

Pre-allow specific tools in command/skill frontmatter (avoid wildcards):
```yaml
allowed-tools:
  - mcp__plugin_csv-demo_csv-tools__describe_csv_file
```

Reference: [MCP tool naming](https://code.claude.com/docs/en/plugins-reference#mcp-servers)

---

## Python dependency pattern
 
`hooks/hooks.json` runs a `Setup` hook that creates a venv in `$CLAUDE_PLUGIN_DATA` on first use.
`.mcp.json` then points `command` to that venv's Python binary:
 
```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_DATA}/venv/bin/python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/src/server.py"]
    }
  }
}
```
 
---
 
## Testing locally
 
```bash
# Load without installing
claude --plugin-dir ./template-plugin
 
# Reload after changing hooks / .mcp.json / agents (SKILL.md changes are live instantly)
/reload-plugins
 
# Validate the manifest
claude plugin validate . --strict
```
 
Reference: [Test plugins locally](https://code.claude.com/docs/en/plugins#test-your-plugins-locally)