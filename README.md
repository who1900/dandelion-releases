# Dandelion rc14: quick start for pilot testers

Dandelion gives your agent a map of project context linked to exact values and
history. Studio lets you explore that memory visually.

Try **one real project over two work sessions**, using **rc14 on Windows 11 with
local Codex**. Other clients and platforms remain unverified.

## 1. Connect once

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and local
Codex. The package is downloaded automatically from a public release link;
no Git installation, repository invitation or GitHub sign-in is needed.

Create a permanent memory folder outside your source repository; it must exist
before the first connection. Add this entry
to `%USERPROFILE%\.codex\config.toml`, substituting the folder's **absolute path**
with doubled backslashes. Edit any existing Dandelion entry instead of duplicating it.

```toml
[mcp_servers.dandelion]
command = "uvx"
args = ["--isolated", "--from", "https://github.com/who1900/dandelion-releases/releases/download/v1.0.0rc14/dandelion-1.0.0rc14-py3-none-any.whl", "--python", "3.13", "dandelion", "serve", "--memory-path", "C:\\path\\to\\existing\\memory", "--local-owner", "--access-mode", "trusted-local", "--lifecycle-v1"]
startup_timeout_sec = 120
```

Reconnect through Codex's MCP controls. The first connection downloads the package,
its dependencies and Python 3.13 if needed; internet access is required.
**Studio is included**; no separate app, database or Dandelion API key is needed.

Chats using this entry share its memory. Use it for the chosen project and keep
the same folder in both sessions; switching projects does not switch memory.

## 2. Work normally, then open Studio

In your project chat, ask:

> Use Dandelion as memory for this project. Read its domain map first. Read this
> project's code and main documentation to organize goals, modules, decisions and
> current work. Keep inspection within this project. Link exact values using the
> references returned by the tools. Preserve sources, uncertainty and history.
> Before changes, read relevant notes; afterward, save what changed and why.
> Keep a short working note for the next session.

Do a real development task, then ask the agent to save progress and the next action.
To see the memory, ask:

> Open Dandelion Studio.

Open the local link. Rotate, zoom and select nodes to inspect notes, facts and
history. Studio refreshes while visible. An initially empty map is normal.

Use **Timeline** to choose a date and inspect recorded changes, available diffs
and author labels. Older unattributed changes say **Author not recorded**.
When a note or value genuinely needs correction, use **Edit note** or **Edit
current value**, give a reason and save. Previous versions and linked history
remain available. Source-managed records and captured originals are not editable
here; ask the agent to use the appropriate memory tools. A revised decision
needs acceptance again. You can also request corrections through the agent.

## 3. Continue in a new session

Start a new project chat with the same MCP entry, without pasting the previous
transcript or record IDs:

> Continue work on [your task]. Start from Dandelion's domain map and working
> note. Explain the current goal, the important decisions and the next action.
> Read linked exact values and relevant history, then check current code as needed.

When real work changes a value, correct the existing fact and inspect its history
in Studio. Do not invent changes for the pilot. After reconnecting MCP, ask to
open Studio again for its current link.

## 4. Send brief feedback

Reply to your inviter or open an [issue](https://github.com/who1900/dandelion-releases/issues/new).
Mark unused features **not tried**.

```text
Environment: Windows version, MCP client/version, agent/model
Release: rc14
Installation and Studio: worked / blocked / not tried; time or error
Real task: one sentence
New session: useful context recovered; missing or wrong details
Exact values/history: worked / blocked / not tried; one example
Studio editing/timeline: worked / blocked / not tried; one example
Expected vs observed: the concrete difference, if any
Would you keep using it? Why?
```

Send a relevant excerpt or screenshot, not your database or credentials.
Failed installations count as feedback too.

## If setup stops

- **Download failed:** check access to the
  [release page](https://github.com/who1900/dandelion-releases/releases/tag/v1.0.0rc14)
  and keep the error. This setup does not require Git credentials.
- **`uvx` not found:** in PowerShell run `(Get-Command uvx).Source`; use that
  absolute path as `command` in the entry, escaping backslashes as above.
- **Startup timeout, client crash or inaccessible tools:** keep the error and
  report it. Do not repeatedly toggle MCP, add another server or delete memory.

Memory retains explicit agent writes; it does not automatically archive chats or
guarantee correct answers. Team cloud sync is outside this pilot.
Keep rc14 fixed during the pilot. A future update replaces only the release
wheel URL in the same MCP entry, followed by a normal reconnect; keep the same
memory folder. Do not add a second server or change the memory path to update.
