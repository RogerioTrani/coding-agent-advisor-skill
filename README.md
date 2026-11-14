# Advisor skill: a stronger model on call for your coding agent

Advisor is an agent skill, a single `SKILL.md` file, that teaches a coding agent to consult a stronger model two or three times per task: before it commits to an approach, when it gets stuck, and before it says the work is done. The agent you already run keeps doing the work. The stronger model reads a short brief and answers with a plan or a correction.

The skill follows the executor and advisor pattern of Anthropic's [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) for the Claude API, and moves it from the API into the agent. It needs no API key and no script. It uses the subagents your coding agent already has.

## Install

The skill is one folder, `skills/advisor`. Every agent below loads it from a skills directory, so installing means copying that folder to the right place. `install.py` does the copy and knows each agent's directory.

```bash
git clone https://github.com/RogerioTrani/coding-agent-advisor-skill
```

```bash
python coding-agent-advisor-skill/install.py --host agents
```

`--host agents` writes to `~/.agents/skills`, the shared directory that Codex, Cursor, GitHub Copilot, Gemini CLI, Kimi Code, Qwen Code, opencode, Codewhale, Devin, Windsurf, Roo Code, Kilo Code, Mistral Vibe, Junie, Goose and Amp all read according to their own documentation. Claude Code reads `~/.claude/skills` instead, so use `--host claude` there. Add `--project` to install into the current repository, or `--dir PATH` for any other location. Without Python, copy the folder by hand: `cp -r coding-agent-advisor-skill/skills/advisor ~/.agents/skills/advisor`.

### Directories by agent

Paths come from each agent's documentation as read in November 2026. Only Claude Code was tested with this skill.

| Agent | User directory (`--host`) | Project directory (`--project`) |
|---|---|---|
| Claude Code (`claude`) | `~/.claude/skills` | `.claude/skills` |
| Codex (`codex`) | `~/.agents/skills` | `.agents/skills` |
| Cursor (`cursor`) | `~/.cursor/skills` | `.cursor/skills` |
| GitHub Copilot (`copilot`) | `~/.copilot/skills` | `.github/skills` |
| Gemini CLI (`gemini`) | `~/.gemini/skills` | `.gemini/skills` |
| Google Antigravity (`antigravity`) | `~/.gemini/config/skills` | `.agents/skills` |
| Kimi Code (`kimi`) | `~/.kimi-code/skills` | `.kimi-code/skills` |
| Qwen Code (`qwen`) | `~/.qwen/skills` | `.qwen/skills` |
| opencode (`opencode`) | `~/.config/opencode/skills` | `.opencode/skills` |
| Codewhale (`codewhale`) | `~/.codewhale/skills` | `.codewhale/skills` |
| Devin (`devin`) | `~/.config/devin/skills`, on Windows `%APPDATA%\devin\skills` | `.agents/skills` |
| Windsurf (`windsurf`) | same as Devin | `.devin/skills` |
| Cline (`cline`) | `~/.cline/skills` | `.cline/skills` |
| Roo Code (`roo`) | `~/.roo/skills` | `.roo/skills` |
| Kilo Code (`kilo`) | `~/.kilo/skills` | `.kilo/skills` |
| Mistral Vibe (`vibe`) | `~/.vibe/skills` | `.vibe/skills` |
| JetBrains Junie (`junie`) | `~/.junie/skills` | `.junie/skills` |
| Kiro (`kiro`) | `~/.kiro/skills` | `.kiro/skills` |
| Amp (`amp`) | `~/.config/agents/skills` | `.agents/skills` |
| Goose (`agents`) | `~/.agents/skills` | `.agents/skills` |

### Install from GitHub without cloning

Some agents install straight from a repository. These commands follow each agent's documentation and have not been run against this repository, except the Claude Code manifest, which passes `claude plugin validate`.

Claude Code:

```
/plugin marketplace add RogerioTrani/coding-agent-advisor-skill
/plugin install advisor@coding-agent-advisor-skill
```

Kimi Code:

```
/plugins install https://github.com/RogerioTrani/coding-agent-advisor-skill
```

GitHub Copilot, with GitHub CLI 2.90 or newer:

```bash
gh skill install RogerioTrani/coding-agent-advisor-skill advisor
```

Amp:

```bash
amp skill add RogerioTrani/coding-agent-advisor-skill
```

Kiro: in the Agent Steering & Skills panel choose Import a skill, then GitHub, and paste `https://github.com/RogerioTrani/coding-agent-advisor-skill/tree/main/skills/advisor`.

### Manifests in this repository

| File | Read by |
|---|---|
| `skills/advisor/agents/openai.yaml` | Codex: display name and default prompt |
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Claude Code plugin marketplace |
| `.codex-plugin/plugin.json` | Codex plugin packaging |
| `.kimi-plugin/plugin.json` | Kimi Code `/plugins` |
| `.cursor-plugin/plugin.json` | Cursor plugins |
| `gemini-extension.json` | Gemini CLI and Qwen Code extensions |
| `plugin.json` | Agent Plugin format, used by Mistral Vibe and Cursor |

### Manus

Manus keeps skills in your account. Download `advisor.skill` from the [latest release](https://github.com/RogerioTrani/coding-agent-advisor-skill/releases/latest), open Skills, choose Add, then Upload a skill.

### Agents without a skills directory

For DeepSeek Harness, Aider, Continue and any agent that only reads a rules file, add this to `AGENTS.md` (or the agent's equivalent) in your project:

```markdown
advisor: consult a stronger model before committing to an approach, when stuck, and before declaring done.
Read skills/advisor/SKILL.md from the coding-agent-advisor-skill repository and follow it.
```

The skill only helps where the agent can start a subagent or a second model session. Where it cannot, the skill tells the agent to say so and continue alone.

## What the agent does with it

1. It orients first: finds the files, reads the source, checks what exists.
2. Before writing anything, it starts a subagent on the strongest model the harness offers and sends a brief: the task, what it found, what it plans to do, what it ruled out, and one question.
3. It does the work, saves it, and runs the tests.
4. Before declaring done, it consults again with what changed and the test output.
5. It tells you in one line what the advisor changed.

It skips the advisor on a one-line edit, a rename, or a factual lookup. If the harness cannot start a second agent, it says so and carries on without one.

## Test results

Three tasks, each run once with the skill and once without. The executor was Claude Sonnet at medium effort inside Claude Code, and the advisor was a Claude Opus subagent.

| Task | With the skill | Without the skill |
|---|---|---|
| Thread-safe sliding window rate limiter for a payments API, with pytest | Two advisor calls. The first replaced per-key locks with a single lock because key eviction could race and admit up to twice the limit. The second caught that the result object was always truthy, so `if limiter.allow(key):` let everything through. 44 tests pass. | No advisor call. Chose a single lock on its own and returned a plain bool. 17 tests pass. |
| Change one timeout value in `config.py` | Edited the line, no advisor call | Edited the line |
| Recommend cookie sessions or Redis sessions for a Flask app | One advisor call before answering | Same recommendation, fewer details |

What these runs do not show: each configuration ran once, so there is no measure of variance. The baseline rate limiter had neither bug the advisor caught, because it made simpler choices from the start. Token counts for the advisor calls were not captured. Only Claude Code was tested.

The test cases are in [`skills/advisor/evals`](skills/advisor/evals) and run with `claude plugin eval`.

## Questions

### What is the advisor pattern for coding agents?

A faster, cheaper model (the executor) does the whole task and consults a more capable model (the advisor) at a few decision points. Most turns of a coding task are mechanical, so the stronger model is paid for only where the approach is decided.

### How is this different from Anthropic's advisor tool?

The advisor tool is a Claude API feature (`advisor_20260301`) that you add to a Messages API request in your own application. The server passes the full transcript to the advisor. This skill gives the same working habit to an agent you use interactively, where that tool is not available. The advisor here is a subagent and sees nothing of the session, so the skill spends a section on how to write the brief.

### Does it need an API key?

No. It uses the subagent or second-model feature of the agent you are already signed in to.

### Which coding agents does it work with?

It was tested in Claude Code. The file follows the Agent Skills format (`SKILL.md` with `name` and `description`), which Codex, Cursor, GitHub Copilot, Gemini CLI, Antigravity, Kimi Code, Qwen Code, opencode, Devin, Windsurf, Cline, Roo Code, Kilo Code, Mistral Vibe, Junie, Kiro, Amp, Goose and Manus document as supported. The install section lists the directory for each one. It only does something useful where the agent can start a subagent or a second model session.

### Does it need a YAML file?

Only Codex reads one: `agents/openai.yaml` inside the skill folder, which sets the display name and default prompt. It is included. The other agents read `SKILL.md` alone, and their plugin manifests are JSON.

### What if my agent already runs the strongest model?

The skill asks for a subagent on the same model with fresh context. A reader who was not inside the reasoning still catches what the executor has stopped seeing.

### How many advisor calls does a task take?

Two on a task longer than a few steps: one before committing to an approach and one before declaring done. More only when the agent is stuck or about to change approach. The skill asks the advisor for answers of about 100 words to keep the cost down.

## License

MIT. See [LICENSE](LICENSE).
