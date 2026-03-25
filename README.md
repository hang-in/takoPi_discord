# takopi-discord

Discord transport plugin for [takopi](https://github.com/banteg/takopi).

This project lets you run takopi agents from Discord text channels, threads, file uploads, and optional voice channels.

## What It Does

`takopi-discord` maps Discord structure to takopi working context:

| Discord | takopi | Meaning |
| --- | --- | --- |
| Server category | visual grouping | organize projects |
| Text channel | project context | one repository or work area |
| Thread | branch/session | one focused task or branch |
| Voice channel | voice session | speech-based interaction |

Typical flow:

1. Bind a Discord channel to a local repository.
2. Send a message in that channel.
3. The bot creates or uses a thread and runs the configured agent.
4. Use `@branch-name` to force work onto a specific branch.
5. Use slash commands to inspect or change behavior.

## Requirements

- Windows, macOS, or Linux
- Python 3.14+
- `git`
- A working takopi installation
- At least one takopi engine installed and available on `PATH`
  - Example: `claude`, `codex`, `opencode`, `pi`
- A Discord bot token

Optional:

- `ffmpeg` for voice-message transcription
- OpenAI API key for text-to-speech in voice channels

## Install From Source

### 1. Clone the Repository

```bash
git clone https://github.com/hang-in/takoPi_discord.git
cd takoPi_discord
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
C:\Python\Python314\python.exe -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Notes:

- Prefer an ASCII-only Python install path on Windows, such as `C:\Python\Python314`.
- If your Python install lives under a non-ASCII user path and launcher issues appear, recreate the venv from an ASCII path Python install.

### 3. Install the Package

Using `uv`:

```bash
uv pip install -e .
```

Or using `pip`:

```bash
python -m pip install -e .
```

### 4. Verify the Environment

```bash
python --version
takopi --version
```

If `takopi` is not found, use the venv-local executable:

Windows:

```powershell
.venv\Scripts\takopi --version
```

macOS/Linux:

```bash
.venv/bin/takopi --version
```

## Discord Bot Setup

### 1. Create the Application

1. Open <https://discord.com/developers/applications>
2. Click `New Application`
3. Give it a name such as `takopi-discord`

### 2. Create the Bot

1. Open the `Bot` tab
2. Click `Reset Token` or `Add Bot`
3. Copy the bot token
4. Keep it private

### 3. Enable Required Privileged Intents

Open the bot settings in the Discord Developer Portal and enable:

- `Message Content Intent`
- `Server Members Intent`

Optional:

- `Presence Intent`

Why:

- `Message Content Intent` is required so the bot can read normal messages.
- `Server Members Intent` is required by the current implementation because the bot requests member intent during startup.
- `Presence Intent` is not required by the current code path, but enabling it does not hurt.

### 4. Invite the Bot

Give the bot at least these permissions:

- View Channels
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Manage Threads
- Read Message History
- Add Reactions
- Attach Files
- Use Slash Commands

Optional voice permissions:

- Connect
- Speak
- Manage Channels

The onboarding flow can generate an invite URL, or you can build one from the application client ID.

## takopi Configuration

### Recommended Repository Layout

Commit `takopi.toml.temp` to git and keep the real `takopi.toml` local only.

- `takopi.toml.temp`: safe template for GitHub
- `takopi.toml`: real local configuration with secrets

### Create `takopi.toml`

Copy the template:

```bash
cp takopi.toml.temp takopi.toml
```

On Windows PowerShell:

```powershell
Copy-Item takopi.toml.temp takopi.toml
```

Then edit `takopi.toml`.

Recommended locations:

- default takopi behavior: copy it to `~/.takopi/takopi.toml`
- project-local workflow: keep it in the repository root if your takopi environment is configured to load local config first

### Minimal Working Example

```toml
transport = "discord"
default_engine = "claude"

[transports.discord]
bot_token = "YOUR_DISCORD_BOT_TOKEN"
guild_id = 1459111087457701952
message_overflow = "split"
session_mode = "stateless"
show_resume_line = true
trigger_mode_default = "all"

[projects.discord]
path = "D:/privateProject/_research/_util/takopi-discord"
worktrees_dir = ".worktrees"
default_engine = "claude"
worktree_base = "main"
```

### Configuration Notes

- `transport = "discord"`
  - tells takopi to start the Discord transport
- `default_engine`
  - default engine when no project or per-channel override is active
- `[transports.discord].bot_token`
  - required Discord bot token
- `[transports.discord].guild_id`
  - optional server restriction; recommended for private use
- `message_overflow = "split"`
  - safer for code-heavy outputs than trimming
- `session_mode = "stateless"`
  - each request is fresh unless resumed from thread/reply context
- `session_mode = "chat"`
  - stores per-channel or per-thread resume tokens
- `[projects.<alias>]`
  - defines reusable local repository contexts

### Optional File Transfer Configuration

```toml
[transports.discord.files]
enabled = true
auto_put = true
auto_put_mode = "upload"
uploads_dir = "incoming"
max_upload_bytes = 20971520
deny_globs = [".git/**", ".env", ".envrc", "**/*.pem", "**/.ssh/**"]
```

### Optional Voice Message Configuration

```toml
[transports.discord.voice_messages]
enabled = true
max_bytes = 10485760
whisper_model = "base"
```

## How Configuration Is Resolved

Safe assumption for public installs:

- takopi reads its config from `~/.takopi/takopi.toml`

If your local takopi setup has been patched or wrapped to prefer project-local config, you may also run from a repository that contains `takopi.toml`.

If you are unsure, place the real config at:

```text
~/.takopi/takopi.toml
```

## Start the Bot

From the project root:

Windows:

```powershell
.venv\Scripts\takopi --transport discord
```

macOS/Linux:

```bash
.venv/bin/takopi --transport discord
```

Expected startup behavior:

1. takopi loads config
2. Discord transport registers slash commands
3. The bot connects to Discord Gateway
4. You should see startup logs such as:
   - `gateway.connecting`
   - `gateway.connected`
   - `bot.ready`

## First-Time Usage in Discord

### 1. Bind a Channel to a Repository

In a Discord text channel:

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

Arguments:

- `project`: local repository path
- `worktrees_dir`: usually `.worktrees`
- `default_engine`: example `claude`
- `worktree_base`: example `main`

Example:

```text
/bind D:/privateProject/_research/_util/takopi-discord .worktrees claude main
```

### 2. Check Status

```text
/status
```

### 3. Send a Normal Prompt

```text
add a detailed README section for installation on Windows
```

### 4. Force a Branch With `@branch`

```text
@feat/readme rewrite the onboarding docs and add examples
```

This creates or uses a thread bound to `feat/readme`.

## Core Slash Commands

### Context and Session

- `/bind <project> [worktrees_dir] [default_engine] [worktree_base]`
- `/unbind`
- `/status`
- `/ctx [show|set|clear]`
- `/new`
- `/cancel`

### Agent and Model Control

- `/agent [show|set|clear] [engine]`
- `/model [engine] [model]`
- `/reasoning [engine] [level]`
- `/trigger [all|mentions|clear]`

### Engine Commands

Dynamic slash commands are registered for every available engine.

Examples:

- `/claude implement the README installation guide`
- `/codex refactor the setup flow`
- `/opencode explain this traceback`

### File Transfer

When enabled:

- `/file get <path>`
- `/file put <path>`

### Voice

When enabled:

- `/voice`
- `/vc`

## Real Usage Examples

### Example 1: Work in the Bound Default Branch

1. Bind the channel:

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

2. Ask:

```text
review the onboarding flow and list user-facing problems
```

The bot uses the channel's default branch, for example `main`.

### Example 2: Start a Branch-Specific Task

```text
@feat/discord-docs add a troubleshooting section for privileged intents
```

This creates a thread bound to `feat/discord-docs`.

### Example 3: Override Engine for One Task

```text
/codex explain why the bot waits forever when startup fails
```

### Example 4: Resume a Session in Chat Mode

If `session_mode = "chat"`, follow up in the same channel or thread:

```text
continue and add tests
```

## Voice Support

Voice support has two separate features.

### Voice Channels

`/voice` creates a temporary voice channel linked to the current text context.

Requirements:

- Discord voice permissions
- local Whisper via `pywhispercpp`
- OpenAI API key for TTS responses

Environment variable:

```bash
OPENAI_API_KEY=your_key_here
```

### Voice Message Attachments

If `[transports.discord.voice_messages]` is enabled, audio attachments in text chat can be transcribed.

Requirements:

- `ffmpeg`
- `pywhispercpp`

## State Files

The transport stores local state in:

- `~/.takopi/discord_state.json`
- `~/.takopi/discord_prefs.json`

These store:

- channel and thread bindings
- per-engine resume tokens
- trigger mode overrides
- default engine overrides
- model and reasoning overrides

Do not commit these files.

## Development

### Editable Install

```bash
uv pip install -e .
```

### Run Tests

```bash
pytest
```

### Lint

```bash
ruff check .
```

## Troubleshooting

### `error: configure discord`

The config file was found but failed Discord setup checks.

Check:

- `transport = "discord"`
- `[transports.discord]` exists
- `bot_token` is present

### `error: invalid takopi config`

The config file exists but failed takopi settings validation.

Check:

- TOML syntax
- engine IDs are valid
- project paths are correct
- the file is being loaded from the directory you expect

### `gateway.start_failed` with `PrivilegedIntentsRequired`

Your Discord bot is missing required privileged intents.

Enable these in the Discord Developer Portal:

- `Message Content Intent`
- `Server Members Intent`

### `gateway.connecting` appears but `bot.ready` never appears

Check:

- bot token is correct
- privileged intents are enabled
- bot was invited to the target server
- firewall or proxy is not blocking Discord

### `lock failed: Permission denied: ~/.takopi/takopi.lock`

takopi could not create its lock file.

Check:

- another takopi process is not already running
- `~/.takopi` is writable
- your shell or sandbox is not blocking writes to the home directory

### `codex not found on PATH`

takopi sees the engine in config but cannot find its CLI.

Install the engine or change `default_engine`.

### Windows launcher issues or broken venv executables

If `.venv\Scripts\takopi` or `.venv\Scripts\python.exe` behaves inconsistently:

1. delete `.venv`
2. recreate it with an ASCII-path Python install such as `C:\Python\Python314`
3. reinstall with `uv pip install -e .`

### `Failed to hardlink files; falling back to full copy`

This is a `uv` performance warning, not a functional failure.

To silence it:

```bash
uv pip install -e . --link-mode=copy
```

or set:

```bash
UV_LINK_MODE=copy
```

## Security Notes

- Never commit `takopi.toml` with a real Discord token.
- Prefer `takopi.toml.temp` for examples.
- Restrict `guild_id` when possible.
- Consider `allowed_user_ids` for private servers.
- Enable file transfer only if you need it.

## Git Ignore Recommendations

This repository ignores:

- `takopi.toml`
- `.venv/`
- `.worktrees/`
- `incoming/`
- `debug.log`

## License

MIT
