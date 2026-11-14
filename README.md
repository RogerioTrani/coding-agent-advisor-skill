# Advisor skill: a stronger model on call for your coding agent

Advisor is an agent skill, a single `SKILL.md` file, that teaches a coding agent to consult a stronger model two or three times per task: before it commits to an approach, when it gets stuck, and before it says the work is done. The agent you already run keeps doing the work. The stronger model reads a short brief and answers with a plan or a correction.

The skill follows the executor and advisor pattern of Anthropic's [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) for the Claude API, and moves it from the API into the agent. It needs no API key and no script. It uses the subagents your coding agent already has.

## Install

Copy the `skills/advisor` folder into your agent's skills folder.

Claude Code, for every project on your machine:

```bash
git clone https://github.com/RogerioTrani/coding-agent-advisor-skill
cp -r coding-agent-advisor-skill/skills/advisor ~/.claude/skills/advisor
```

Agents that read skills from `.agents/skills`, for one project:

```bash
cp -r coding-agent-advisor-skill/skills/advisor .agents/skills/advisor
```

Codex, for every project on your machine:

```bash
cp -r coding-agent-advisor-skill/skills/advisor ~/.agents/skills/advisor
```

The folder includes `agents/openai.yaml`, the metadata file Codex reads for the skill's display name and default prompt. Other agents ignore it.

The skill is plain Markdown. If your agent has no skills folder, paste the body of [`skills/advisor/SKILL.md`](skills/advisor/SKILL.md) into its rules file (`AGENTS.md`, `CLAUDE.md`, or the equivalent).

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

It was tested in Claude Code. The file follows the Agent Skills format (`SKILL.md` with `name` and `description`), so agents that load that format can read it. It only does something useful where the agent can start a subagent or a second model session.

### What if my agent already runs the strongest model?

The skill asks for a subagent on the same model with fresh context. A reader who was not inside the reasoning still catches what the executor has stopped seeing.

### How many advisor calls does a task take?

Two on a task longer than a few steps: one before committing to an approach and one before declaring done. More only when the agent is stuck or about to change approach. The skill asks the advisor for answers of about 100 words to keep the cost down.

## License

MIT. See [LICENSE](LICENSE).
