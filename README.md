# Try Dandelion rc23 on your own project

Pick one unfinished task you would normally work on across two sessions. The pilot runs on Windows 11 with local Codex. Use a project you can inspect and a dedicated memory folder for it. Independent solo use is free. For a team trial, contact danik1900@gmail.com. [License](https://github.com/who1900/dandelion-releases/blob/main/LICENSING.md)

## 1. Connect once

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed. Open the intended project folder in Codex.

- **Already used Dandelion on this project?** Keep the existing `--memory-path` and registration. Check the path in the entry and skip folder creation. The same folder carries the project's history across chats and package updates.
- **First time using Dandelion on this project?** Choose a unique folder name, whether the repository is empty or years old. Replace `my-project` below with that name and run this in PowerShell. Pick a different name if another project already uses it.

```powershell
$memoryPath = Join-Path $env:LOCALAPPDATA 'Dandelion\workspaces\my-project'
(New-Item -ItemType Directory -Force -Path $memoryPath).FullName
```

For a fresh registration, put the entry below in `.codex/config.toml` inside the trusted project folder (create the directory and file if needed). Keep this machine-specific path local. Replace `PASTE_FOLDER_PATH_HERE` with the printed path, keeping the single quotes.

An entry in `%USERPROFILE%\.codex\config.toml` is user-wide: opening another repository still uses that folder. If this project already uses that entry, keep it for this pilot. For a different project, configure its own project-local entry under the same name, with its own path. Leave the first project's path intact.

```toml
[mcp_servers.dandelion]
command = "uvx"
args = ["--isolated", "--from", "dandelion-memory==1.0.0rc23", "--python", "3.13", "dandelion", "serve", "--memory-path", 'PASTE_FOLDER_PATH_HERE', "--local-owner", "--access-mode", "trusted-local", "--lifecycle-v1"]
startup_timeout_sec = 120
```

After a configuration change, use **Restart** beside **Servers** in Codex MCP settings. The first connection downloads rc23 from PyPI and includes Studio. Before saving anything, ask the agent to call `domain_map` and open Studio with `open_studio`. Check the **Workspace** name against the memory folder you chose. Fresh memory starts with an empty map, even in a mature repository. Returning to an existing memory should show its familiar domains. If either looks unexpected, check the configured path before continuing.

## 2. Build the map while doing real work

Choose the prompt that fits your project:

**Starting a new project**

> My first task is [task]. The goal is [goal] and the constraint is [constraint]. Start the work. In Dandelion, save the first decision we actually make, its reason, and any question we leave open. Before we stop, save the next concrete action.

**Working in an existing project**

> Continue [real task]. Read the Dandelion map, then inspect the relevant code and docs. Map the parts this task touches. Save decisions and their reasons where a source supports them. Link exact values and attach an original excerpt when wording matters. Flag what is still unknown. Start the work and save where to resume.

In Studio, select a node for your task and read it in **Inspector**. If a detail needs correcting, edit it and give the reason. **Timeline** shows the recorded change.

## 3. Continue in a fresh chat

Open a new Codex chat in the same project with the same MCP entry. Give it only the task name. Leave the old transcript, note IDs and your own recap out of the prompt.

> Continue [task name]. Use Dandelion to recover where we left off and why. Tell me the next step, check it against the current code, and carry it out. Save the outcome for the next session.

**Send your inviter three lines:** Did installation and Studio work? What did the new agent recover correctly? What did you have to repeat or correct? If setup failed, include the error with private paths or credentials removed.

## 4. Try two lookups in a separate test memory

After the real task, open an empty test project in Codex. Follow step 1 with a **new, empty memory folder** (for example, `pilot-probe-01`) and a project-local MCP entry. Confirm that Studio shows that workspace before writing. Leave your real project's settings and memory as they are.

**Setup chat.** Give the agent this prompt once:

> Create two separate exact facts with `create_fact`. Use the identical subject `pilot.worker.port` for both, with values `8080` and `9090`. Check that the returned keys differ. Then use `get_fact` by name to verify that `pilot.worker.port` returns `AMBIGUOUS_NAME` with those two keys and `pilot.scheduler.port` returns `FACT_NOT_FOUND`. Report whether setup succeeded.

If setup fails, report the setup issue and stop the probe. Once it succeeds, open a **fresh chat in the test project**. Give the agent only these questions, one at a time:

1. What value does Dandelion have for `pilot.scheduler.port`?
2. What value does Dandelion have for `pilot.worker.port`?

For each question, note the agent's first response before helping. Send your inviter one line per name: **What did the agent do next? Did you have to step in, and if so, how?** Keep these observations separate from feedback on your real task.
