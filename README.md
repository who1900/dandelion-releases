# Try Dandelion rc21 on your own project

Pick one unfinished task you would normally work on across two sessions. The pilot runs on Windows 11 with local Codex. Use a project you can inspect and a dedicated memory folder for it. Independent solo use is free. For a team trial, contact danik1900@gmail.com. [License](https://github.com/who1900/dandelion-releases/blob/main/LICENSING.md)

## 1. Connect once

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed. Create a permanent folder outside your repository for this project's memory. In PowerShell:

```powershell
$memoryPath = Join-Path $env:LOCALAPPDATA 'Dandelion\workspaces\my-project'
(New-Item -ItemType Directory -Force -Path $memoryPath).FullName
```

In `%USERPROFILE%\.codex\config.toml`, add the entry below. Replace `PASTE_FOLDER_PATH_HERE` with the printed path, keeping the single quotes. If Dandelion is already registered for this project, keep its folder and change only the package version in the existing entry.

```toml
[mcp_servers.dandelion]
command = "uvx"
args = ["--isolated", "--from", "dandelion-memory==1.0.0rc21", "--python", "3.13", "dandelion", "serve", "--memory-path", 'PASTE_FOLDER_PATH_HERE', "--local-owner", "--access-mode", "trusted-local", "--lifecycle-v1"]
startup_timeout_sec = 120
```

Apply the change in Codex MCP settings using **Restart** beside **Servers**. The first connection downloads rc21 from PyPI and includes Studio. Ask your agent to **call `domain_map`**. An empty map is a successful connection to fresh memory. Chats using this entry share its folder.

## 2. Build the map while doing real work

Open the project in Codex. Replace the brackets and give your agent this prompt:

> My task is [real task]. Read the Dandelion map, then inspect the README and the code and docs relevant to this task. Build a small map using the project's own names. Record how the relevant parts fit together and why important decisions were made. Link exact values to their sources. Attach a short original excerpt when its wording matters. Flag anything you could not verify. Start the task. Before we stop, save what changed, what is still open, and the next concrete action.

Ask **“Open Dandelion Studio using `open_studio`.”** Open the returned local link. Select a node for your task and read it in **Inspector**. If a detail needs correcting, edit it and give the reason. **Timeline** shows the recorded change.

## 3. Continue in a fresh chat

Open a new Codex chat in the same project with the same MCP entry. Give it only the task name. Leave the old transcript, note IDs and your own recap out of the prompt.

> Continue [task name]. Use Dandelion to recover where we left off and why. Tell me the next step, check it against the current code, and carry it out. Save the outcome for the next session.

**Send your inviter three lines:** Did installation and Studio work? What did the new agent recover correctly? What did you have to repeat or correct? If setup failed, include the error with private paths or credentials removed.
