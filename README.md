# takopi-discord

Standalone Discord coding-agent bridge with vendored `takopi` core.

## Claude Code Must-Know

Before Claude Code edits or sets up this repository, it should assume all of the following:

- This repository is for Discord transport only.
- Real local secrets must go in `takopi.toml`, not in `takopi.toml.temp`.
- `takopi.toml.temp` is the public template that should be copied and filled in locally.
- `transport = "discord"` is the intended runtime mode.
- This repository includes the core runtime it needs.
- In `session_mode = "chat"`, plain channel conversations should stay in the same Discord channel and should not auto-create a new thread for each message.
- `@branch-name` is the explicit signal for branch/thread-oriented work.
- Do not commit bot tokens, API keys, local absolute paths, `discord_state.json`, `takopi.lock`, or other local runtime artifacts.
- The primary CLI is `takopi-discord`.

## Claude Code Quick Start

If you cloned this repository and want Claude Code to install and configure it for you, run Claude Code in the repository root and give it the handoff prompt below.

Example:

```bash
git clone https://github.com/hang-in/takoPi_discord.git
cd takoPi_discord
claude
```

Paste this prompt into Claude Code:

```text
Read README.md completely, then set up this repository for local use.

Tasks:
1. Verify Python and virtualenv state.
2. Install dependencies in the local .venv.
3. Create takopi.toml from takopi.toml.temp if it does not exist.
4. Explain which values I must fill in manually, especially Discord bot token, guild ID, and local project path.
5. Verify the bot can start, and show me the exact next command to run.

Important constraints:
- Follow the README exactly.
- Assume I want Discord only.
- Use the standalone `takopi-discord` CLI from this repository.
- Do not commit secrets.
```

---

## 한국어 가이드

### 개요

`takopi-discord`는 vendored core를 포함한 독립 실행형 Discord 코딩 에이전트 브리지입니다.

주요 동작 방식:

- Discord 텍스트 채널을 로컬 프로젝트와 연결
- 메시지를 보내면 내장 런타임 기반 agent가 실행
- `@branch-name` 형식으로 브랜치를 지정하면 해당 브랜치용 thread 작업 가능
- slash command로 상태, 엔진, 모델, 트리거 모드 등을 제어
- 선택적으로 파일 업로드/다운로드, 음성 채널, 음성 메시지 전사 지원

매핑 개념:

| Discord | 내부 런타임 | 설명 |
| --- | --- | --- |
| Text channel | project context | 로컬 저장소 하나 |
| Thread | branch/session | 작업 단위 또는 브랜치 단위 대화 |
| Voice channel | voice session | 음성 대화 세션 |

### 요구 사항

- Python 3.14 이상
- `git`
- 동작 가능한 `takopi-discord` 실행 환경
- 최소 1개 이상의 지원 엔진 CLI
  - 예: `claude`, `codex`, `opencode`, `pi`
- Discord bot token

선택 사항:

- `ffmpeg`
- `OPENAI_API_KEY` (음성 채널 TTS 용도)

### 설치

#### 1. 저장소 클론

```bash
git clone https://github.com/hang-in/takoPi_discord.git
cd takoPi_discord
```

#### 2. 가상환경 생성

Windows PowerShell:

```powershell
C:\Python\Python314\python.exe -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

권장:

- Windows에서는 가능하면 ASCII 경로의 Python 설치를 사용하세요.
- 예: `C:\Python\Python314`
- 사용자 홈 경로에 한글이 포함된 Python 설치는 launcher 문제를 일으킬 수 있습니다.

#### 3. 패키지 설치

```bash
uv pip install -e .
```

또는:

```bash
python -m pip install -e .
```

#### 4. 설치 확인

```bash
python --version
takopi-discord --version
```

필요하면 venv 내부 실행 파일을 직접 사용하세요.

Windows:

```powershell
.venv\Scripts\takopi-discord --version
```

### Discord 봇 설정

#### 1. Discord Developer Portal에서 Application 생성

1. <https://discord.com/developers/applications> 접속
2. `New Application` 클릭
3. 앱 이름 입력

#### 2. Bot 생성

1. `Bot` 탭 이동
2. `Add Bot` 또는 `Reset Token`
3. bot token 복사

#### 3. Privileged Intents 활성화

현재 코드 기준으로 아래 두 개는 반드시 켜는 것을 권장합니다.

- `Message Content Intent`
- `Server Members Intent`

있어도 문제 없는 항목:

- `Presence Intent`

이유:

- `Message Content Intent`: 일반 메시지 내용을 읽기 위해 필요
- `Server Members Intent`: 현재 구현이 member intent를 요청함

#### 4. Bot 권한

최소 권장 권한:

- View Channels
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Manage Threads
- Read Message History
- Add Reactions
- Attach Files
- Use Slash Commands

음성 기능을 쓸 경우 추가:

- Connect
- Speak
- Manage Channels

### 설정 파일 작성

#### 중요한 제한 사항

이 저장소는 필요한 core를 내부에 포함합니다.
별도의 외부 `takopi` 설치 없이 `takopi-discord` CLI만 기준으로 설정하면 됩니다.

#### `takopi.toml` 생성

```bash
cp takopi.toml.temp takopi.toml
```

Windows PowerShell:

```powershell
Copy-Item takopi.toml.temp takopi.toml
```

권장 위치:

- 프로젝트 루트 `takopi.toml`

#### 최소 동작 예시

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

설명:

- `[transports.discord]`: 실제 Discord 실행 설정
- `[projects.discord]`: 로컬 프로젝트 경로와 worktree 기본값

#### 선택 설정: 파일 전송

```toml
[transports.discord.files]
enabled = true
auto_put = true
auto_put_mode = "upload"
uploads_dir = "incoming"
max_upload_bytes = 20971520
deny_globs = [".git/**", ".env", ".envrc", "**/*.pem", "**/.ssh/**"]
```

#### 선택 설정: 음성 메시지 전사

```toml
[transports.discord.voice_messages]
enabled = true
max_bytes = 10485760
whisper_model = "base"
```

### 실행

Windows:

```powershell
.venv\Scripts\takopi-discord --transport discord
```

macOS / Linux:

```bash
.venv/bin/takopi-discord --transport discord
```

정상 로그 예시:

- `gateway.connecting`
- `gateway.connected`
- `bot.ready`

### Discord에서 최초 사용 방법

#### 1. 채널을 로컬 프로젝트와 바인딩

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

보다 명시적으로:

```text
/bind D:/privateProject/_research/_util/takopi-discord .worktrees claude main
```

#### 2. 상태 확인

```text
/status
```

#### 3. 일반 작업

```text
README 설치 가이드를 윈도우 기준으로 더 자세히 써줘
```

#### 4. 브랜치 지정 작업

```text
@feat/readme-docs 설치 문서를 전면 개편해줘
```

이 경우 해당 브랜치 기준 thread 작업이 시작됩니다.

### 주요 Slash Command

- `/bind <project> [worktrees_dir] [default_engine] [worktree_base]`
- `/unbind`
- `/status`
- `/ctx [show|set|clear]`
- `/new`
- `/cancel`
- `/agent [show|set|clear] [engine]`
- `/model [engine] [model]`
- `/reasoning [engine] [level]`
- `/trigger [all|mentions|clear]`

동적 엔진 명령 예시:

- `/claude ...`
- `/codex ...`
- `/opencode ...`

### 실사용 예시

#### 예시 1. 기본 브랜치에서 작업

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

```text
온보딩 흐름의 사용자 문제점을 정리해줘
```

#### 예시 2. 특정 브랜치에서 작업

```text
@feat/discord-onboarding privileged intents 관련 트러블슈팅 섹션 추가해줘
```

#### 예시 3. 특정 엔진으로만 실행

```text
/codex 왜 startup 실패 시 이전에는 로그가 안 보였는지 설명해줘
```

### 상태 파일

로컬 상태 파일:

- 프로젝트 루트 `discord_state.json`
- 프로젝트 루트 `discord_prefs.json`

저장 내용:

- 채널/스레드 바인딩
- resume token
- trigger mode override
- default engine override
- model / reasoning override

### 장애 대응

#### `error: configure discord`

확인 항목:

- `transport = "discord"`
- `[transports.discord]` 존재
- `bot_token` 존재

#### `error: invalid takopi config`

확인 항목:

- TOML 문법
- engine ID 오타
- 프로젝트 경로

#### `PrivilegedIntentsRequired`

Discord Developer Portal에서 아래를 켜세요.

- `Message Content Intent`
- `Server Members Intent`

#### `gateway.connecting` 후 `bot.ready`가 안 나옴

확인 항목:

- bot token이 맞는지
- privileged intents가 켜졌는지
- 봇이 해당 서버에 초대되었는지
- 네트워크/방화벽 문제

#### `lock failed: Permission denied`

확인 항목:

- 다른 `takopi-discord` 프로세스가 이미 실행 중인지
- 프로젝트 디렉터리 쓰기 권한이 있는지

#### Windows에서 `.venv` 런처가 이상함

권장 절차:

1. `.venv` 삭제
2. ASCII 경로 Python으로 재생성
3. `uv pip install -e .` 재실행

#### `Failed to hardlink files; falling back to full copy`

기능 오류가 아니라 `uv` 성능 경고입니다.

```bash
uv pip install -e . --link-mode=copy
```

### 보안 주의

- 실제 token이 들어간 `takopi.toml`은 커밋하지 마세요.
- `takopi.toml.temp`만 예시로 올리세요.
- 가능하면 `guild_id`를 제한하세요.
- 필요 없으면 파일 전송 기능은 끄세요.

---

## English Guide

### Overview

`takopi-discord` is a standalone Discord coding-agent bridge with vendored `takopi` core.

It lets you:

- bind Discord channels to local repositories
- run the bundled agent runtime from Discord messages
- use branch-specific threads with `@branch-name`
- control engine, model, trigger mode, and session behavior with slash commands
- optionally use file transfer, voice channels, and voice-message transcription

Mapping:

| Discord | Internal runtime | Meaning |
| --- | --- | --- |
| Text channel | project context | one repository |
| Thread | branch/session | task or branch-scoped conversation |
| Voice channel | voice session | speech-based interaction |

### Requirements

- Python 3.14+
- `git`
- working `takopi-discord` environment
- at least one installed supported engine CLI
- a Discord bot token

Optional:

- `ffmpeg`
- `OPENAI_API_KEY` for TTS in voice channels

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/hang-in/takoPi_discord.git
cd takoPi_discord
```

#### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
C:\Python\Python314\python.exe -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Recommended:

- On Windows, prefer an ASCII-only Python installation path.
- Example: `C:\Python\Python314`

#### 3. Install the Package

```bash
uv pip install -e .
```

Or:

```bash
python -m pip install -e .
```

#### 4. Verify

```bash
python --version
takopi-discord --version
```

If needed, call the venv-local executable directly:

Windows:

```powershell
.venv\Scripts\takopi-discord --version
```

### Discord Bot Setup

#### 1. Create the Application

1. Open <https://discord.com/developers/applications>
2. Click `New Application`
3. Give it a name

#### 2. Create the Bot

1. Open the `Bot` tab
2. Create or reset the bot token
3. Copy the token

#### 3. Enable Required Privileged Intents

Enable:

- `Message Content Intent`
- `Server Members Intent`

Optional:

- `Presence Intent`

#### 4. Bot Permissions

Recommended minimum permissions:

- View Channels
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Manage Threads
- Read Message History
- Add Reactions
- Attach Files
- Use Slash Commands

Optional for voice:

- Connect
- Speak
- Manage Channels

### Configuration

#### Important Current Limitation

This repository vendors the core runtime it needs.
You do not need a separate external `takopi` installation.

#### Create `takopi.toml`

```bash
cp takopi.toml.temp takopi.toml
```

Windows PowerShell:

```powershell
Copy-Item takopi.toml.temp takopi.toml
```

Recommended location:

- project-root `takopi.toml`

#### Minimal Working Example

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

#### Optional File Transfer

```toml
[transports.discord.files]
enabled = true
auto_put = true
auto_put_mode = "upload"
uploads_dir = "incoming"
max_upload_bytes = 20971520
deny_globs = [".git/**", ".env", ".envrc", "**/*.pem", "**/.ssh/**"]
```

#### Optional Voice Message Transcription

```toml
[transports.discord.voice_messages]
enabled = true
max_bytes = 10485760
whisper_model = "base"
```

### Start the Bot

Windows:

```powershell
.venv\Scripts\takopi-discord --transport discord
```

macOS / Linux:

```bash
.venv/bin/takopi-discord --transport discord
```

Expected logs:

- `gateway.connecting`
- `gateway.connected`
- `bot.ready`

### First-Time Usage in Discord

#### 1. Bind a Channel

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

More explicit example:

```text
/bind D:/privateProject/_research/_util/takopi-discord .worktrees claude main
```

#### 2. Check Status

```text
/status
```

#### 3. Send a Prompt

```text
Rewrite the installation section for Windows users.
```

#### 4. Use a Branch-Specific Thread

```text
@feat/readme-docs rewrite onboarding and troubleshooting docs
```

### Main Slash Commands

- `/bind <project> [worktrees_dir] [default_engine] [worktree_base]`
- `/unbind`
- `/status`
- `/ctx [show|set|clear]`
- `/new`
- `/cancel`
- `/agent [show|set|clear] [engine]`
- `/model [engine] [model]`
- `/reasoning [engine] [level]`
- `/trigger [all|mentions|clear]`

Dynamic engine examples:

- `/claude ...`
- `/codex ...`
- `/opencode ...`

### Real Usage Examples

#### Example 1. Work on the default branch

```text
/bind D:/privateProject/_research/_util/takopi-discord
```

```text
Review the onboarding flow and list user-facing problems.
```

#### Example 2. Work on a specific branch

```text
@feat/discord-onboarding add a troubleshooting section for privileged intents
```

#### Example 3. Use a specific engine

```text
/codex explain why startup failures used to be silent
```

### State Files

Local state is stored in:

- project-root `discord_state.json`
- project-root `discord_prefs.json`

### Troubleshooting

#### `error: configure discord`

Check:

- `transport = "discord"`
- `[transports.discord]` exists
- `bot_token` exists

#### `error: invalid takopi config`

Check:

- TOML syntax
- engine IDs
- project path

#### `PrivilegedIntentsRequired`

Enable in Discord Developer Portal:

- `Message Content Intent`
- `Server Members Intent`

#### `gateway.connecting` appears but `bot.ready` does not

Check:

- token correctness
- privileged intents
- bot invite
- firewall or network restrictions

#### `lock failed: Permission denied`

Check:

- another `takopi-discord` process is already running
- the project directory is writable

#### Broken venv launcher on Windows

Recommended recovery:

1. delete `.venv`
2. recreate it with an ASCII-path Python install
3. reinstall with `uv pip install -e .`

#### `Failed to hardlink files; falling back to full copy`

This is a `uv` performance warning, not a functional failure.

```bash
uv pip install -e . --link-mode=copy
```

### Security Notes

- Never commit a real `takopi.toml` with secrets.
- Commit `takopi.toml.temp` instead.
- Restrict `guild_id` when possible.
- Enable file transfer only when needed.

## License

MIT
