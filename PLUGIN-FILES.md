# How Claude Code manages plugin files

The plugin lifecycle, step by step, using this plugin (`csv-demo@template-plugin`) as the example.
Verified against the [plugins reference](https://code.claude.com/docs/en/plugins-reference#environment-variables)
and [marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces), plus inspection of a real install.

## Step 1 — `/plugin marketplace add barbiquilmes/template-plugin`

Clones the marketplace repo to `~/.claude/plugins/marketplaces/<marketplace>/` and registers it in
`~/.claude/plugins/known_marketplaces.json`. This is catalog-only: **no plugin is installed yet**.
`/plugin marketplace update` refreshes this local copy.

## Step 2 — `/plugin install csv-demo@template-plugin`

Copies the plugin files into the versioned **plugin cache**:

```
~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/
                        template-plugin/csv-demo/0.1.0/     ← this plugin
```

Marketplace plugins are always copied here (for security and verification) rather than run in place.
Consequence: paths that traverse outside the plugin root (e.g. `../shared-utils`) break after
installation, because those files are never copied into the cache.

## Step 3 — Runtime: the two environment variables

| Variable | Points to | Survives update? |
|---|---|---|
| `CLAUDE_PLUGIN_ROOT` | The cache dir from step 2 | No — path changes each version |
| `CLAUDE_PLUGIN_DATA` | `~/.claude/plugins/data/<id>/` | Yes |

`<id>` is the plugin identifier (`csv-demo@template-plugin`) with every character outside
`a-z A-Z 0-9 _ -` replaced by `-` → `csv-demo-template-plugin`. The directory is created lazily,
the first time `${CLAUDE_PLUGIN_DATA}` is actually referenced.

Both variables are substituted into hook commands, MCP/LSP server configs, and monitor commands,
and are set in the processes those spawn. They are **not** set in your interactive shell.

Treat `ROOT` as read-only source code; put venvs, caches, and generated state in `DATA`.

## Step 4 — Update

A new `<version>/` directory appears in the cache and `CLAUDE_PLUGIN_ROOT` moves to it;
`CLAUDE_PLUGIN_DATA` is untouched. The old version directory is marked orphaned and deleted
automatically **about 7 days later** — the grace period lets sessions still running the old
version keep working. Mid-session, hooks and MCP servers keep using the old path until you run
`/reload-plugins` (monitors need a session restart).

## Step 5 — `/plugin uninstall`

The cache entry is orphaned (same 7-day cleanup). The data directory is deleted when you
uninstall from the **last scope** where the plugin is installed: the `/plugin` UI shows its size
and prompts first; the CLI deletes by default unless you pass `--keep-data`.

## Local development is different

`claude --plugin-dir ./template-plugin` loads the plugin **in place** — no marketplace, no cache
copy, no version directory. That's why edits show up without reinstalling.
