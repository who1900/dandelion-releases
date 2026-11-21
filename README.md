# Try Dandelion rc23 on your own project

Pick one unfinished task you would normally work on across two sessions. You can join with any agent client that can launch a **local stdio MCP server**. Windows 11 with local Codex is the verified rc23 setup. Other OS and client combinations are welcome; tell your inviter which you use. Independent solo use is free. For a team trial, contact danik1900@gmail.com. [License](https://github.com/who1900/dandelion-releases/blob/main/LICENSING.md)

## 1. Connect once

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed. Open your project in your agent client.

- **Already used Dandelion on this project?** Keep the existing `--memory-path` and registration. Check the path in the entry and skip folder creation. The same folder carries the project's history across chats and package updates.
- **First time using Dandelion on this project?** Create an empty, permanent folder for its memory, outside your repository. Give it a unique project name. Use your file manager and copy the absolute path, or use the Windows example below with your own project name.

```powershell
$memoryPath = Join-Path $env:LOCALAPPDATA 'Dandelion\workspaces\my-project'
(New-Item -ItemType Directory -Force -Path $memoryPath).FullName
```

**In your client's MCP settings**, choose a local stdio server named `dandelion`. Set the command to `uvx` and use these arguments in order, one entry per argument. Replace the placeholder with the absolute path to the folder you chose. If your client cannot find `uvx`, use the full path printed by `command -v uvx` (macOS/Linux) or `(Get-Command uvx).Source` (Windows PowerShell).

```json
["--isolated", "--from", "dandelion-memory==1.0.0rc23", "--python", "3.13", "dandelion", "serve", "--memory-path", "PASTE_FOLDER_PATH_HERE", "--local-owner", "--access-mode", "trusted-local", "--lifecycle-v1"]
```

**Codex example.** If you use Codex, you can enter the same settings in `.codex/config.toml` inside the trusted project folder. Keep this machine-specific path local. An existing user-wide entry uses the same memory across projects. Keep its path when returning to a project.

```toml
[mcp_servers.dandelion]
command = "uvx"
args = ["--isolated", "--from", "dandelion-memory==1.0.0rc23", "--python", "3.13", "dandelion", "serve", "--memory-path", 'PASTE_FOLDER_PATH_HERE', "--local-owner", "--access-mode", "trusted-local", "--lifecycle-v1"]
startup_timeout_sec = 120
```

Apply the settings and connect using your client's MCP controls (in Codex, **Restart** beside **Servers**). The first connection downloads rc23 from PyPI and includes Studio. Before saving anything, ask the agent to call `domain_map` and open Studio with `open_studio`. Check the **Workspace** name against the memory folder you chose. Fresh memory starts with an empty map, even in a mature repository. Returning to an existing memory should show its familiar domains. If either looks unexpected, check the configured path before continuing.

## 2. Build the map while doing real work

Choose the prompt that fits your project:

**Starting a new project**

> My first task is [task]. The goal is [goal] and the constraint is [constraint]. Start the work. In Dandelion, save the first decision we actually make, its reason, and any question we leave open. Before we stop, save the next concrete action.

**Working in an existing project**

> Continue [real task]. Read the Dandelion map, then inspect the relevant code and docs. Map the parts this task touches. Save decisions and their reasons where a source supports them. Link exact values and attach an original excerpt when wording matters. Flag what is still unknown. Start the work and save where to resume.

In Studio, select a node for your task and read it in **Inspector**. If a detail needs correcting, edit it and give the reason. **Timeline** shows the recorded change.

## 3. Continue in a fresh chat

Start a fresh session in your client with the same project and memory folder. Give it only the task name. Leave the old transcript, note IDs and your own recap out of the prompt.

> Continue [task name]. Use Dandelion to recover where we left off and why. Tell me the next step, check it against the current code, and carry it out. Save the outcome for the next session.

**Send your inviter three lines:** Did installation and Studio work? What did the new agent recover correctly? What did you have to repeat or correct? If setup failed, include the error with private paths or credentials removed.

## 4. Try two lookups in a separate test memory

After the real task, open an empty test project in your client. Follow step 1 with a **new, empty memory folder** (for example, `pilot-probe-01`). Prefer project-local settings. If your client has only one global entry, save the real project's path, disconnect, change `--memory-path` to the test folder and reconnect. Confirm the test workspace in Studio before writing. Restore the real path and reconnect when you finish the probe.

**Setup chat.** Give the agent this prompt once:

> Create two separate exact facts with `create_fact`. Use the identical subject `pilot.worker.port` for both, with values `8080` and `9090`. Check that the returned keys differ. Then use `get_fact` by name to verify that `pilot.worker.port` returns `AMBIGUOUS_NAME` with those two keys and `pilot.scheduler.port` returns `FACT_NOT_FOUND`. Report whether setup succeeded.

If setup fails, report the setup issue and stop the probe. Once it succeeds, open a **fresh chat in the test project**. Give the agent only these questions, one at a time:

1. What value does Dandelion have for `pilot.scheduler.port`?
2. What value does Dandelion have for `pilot.worker.port`?

For each question, note the agent's first response before helping. Send your inviter one line per name: **What did the agent do next? Did you have to step in, and if so, how?** Keep these observations separate from feedback on your real task.
