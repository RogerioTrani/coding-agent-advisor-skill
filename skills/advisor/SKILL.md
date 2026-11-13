---
name: advisor
description: Pair yourself (the executor) with a stronger reviewer model that you consult at a few key moments of a coding task - before committing to an approach, when stuck, and before declaring done. Use this skill on any coding or agentic task longer than a few steps, on design, architecture and risk questions, when errors keep recurring or an approach is not converging, and whenever the user mentions an advisor, a second opinion, a stronger model, or a plan review. Works in any coding agent that can start a subagent or a second model session.
---

# Advisor

You are the executor: you do the work. An advisor is a stronger model you consult briefly, a few times per task, for a plan or a course correction. Most turns of a coding task are mechanical; what decides the outcome is the approach. Two or three well-timed consultations buy most of the quality of running the stronger model throughout, at a fraction of the cost.

The advisor only advises. It does not write the deliverable, edit files, or talk to the user. You stay responsible for the result.

## Reaching the advisor

Use what your harness already has. In order of preference:

1. A subagent or secondary agent running on a model stronger than yours (the top tier your harness offers).
2. If you already are the strongest model available, a subagent on your own model with fresh context. A reader who has not been inside your reasoning still catches what you have stopped seeing.

Give the advisor read-only work: it reads, thinks, and answers. Ask for the reasoning effort your user's standing instructions allow; do not raise it on your own.

If your harness has no way to start a second agent or model, say so to the user in one line and carry on without an advisor. Do not role-play one: advice you write to yourself looks like a second opinion and is not.

## When to consult

Consult **before substantive work**: before writing, before committing to an interpretation, before building on an assumption. Orient first if the task needs it (find the files, read the source, see what is there), then consult. Orientation is not substantive work. Writing, editing, and declaring an answer are.

Also consult:

- **When you believe the task is complete.** First make the deliverable durable: write the file, save the result, commit if the user asked for commits. A consultation takes time, and a saved result survives an interrupted session.
- **When stuck**: errors recurring, an approach not converging, results that do not fit.
- **When considering a change of approach.**
- **On design, architecture, and risk questions** where your whole answer would be analysis or a recommendation. That judgment call is where a second opinion is worth most.

On a task longer than a few steps, that means at least once before committing to an approach and once before declaring done. If you also keep a task list or a written plan, consult first so the advice shapes the plan.

Skip the advisor when there is nothing to plan: a one-line edit, a rename, a factual lookup, or a short reactive step where the tool output you just read dictates the next action. The first consultation, before the approach hardens, carries most of the value; do not keep calling out of habit.

## The brief

The advisor sees nothing of your session. Whatever you leave out of the brief does not exist for it, so the brief decides how good the advice can be. Write it in your own words and include:

- The task as the user stated it, with their constraints and preferences.
- What you found during orientation: the relevant files and paths, the facts that matter, quoted where exact wording matters (error messages, signatures, test output).
- What you intend to do, or what you did, and why.
- What you already tried or ruled out, so it is not suggested again.
- The specific question: "is this the right approach?", "what am I missing?", "why does this keep failing?", "is this done?".
- The length you want back. Ask for a focused answer of about 100 words for a starting point, more for a final review. Advice is paid for at the stronger model's rate, and a short pointed answer is also easier to act on.

Point the advisor at files to read instead of pasting them when it can read the workspace. State your plan as a plan, not as a conclusion to confirm: an advisor handed a conclusion tends to return it confirmed.

## Using the advice

Give the advice serious weight. Adapt only when a step fails empirically, or when primary-source evidence contradicts a specific claim (the file says X, the documentation states Y). A passing self-test is not evidence the advice is wrong; it is evidence your test does not check what the advice is checking.

If you already hold evidence pointing one way and the advisor points another, do not switch silently and do not ignore it. Go back once with the conflict stated: "I found X, you suggest Y, which constraint breaks the tie?" A reconcile call costs less than committing to the wrong branch.

Tell the user, in a line, when the advisor changed your approach and how. Do not paste the advice wholesale; report the decision.

## Example

Task: add retry with backoff to an HTTP client used by twelve call sites.

1. Orient: read the client, list the call sites, check for existing retry code and tests.
2. Consult: brief with the task, the twelve call sites, the one that already retries by hand, the plan (wrap the transport), and the question "what breaks if retries are added at the transport level?". Ask for about 100 words.
3. The advisor flags non-idempotent POSTs. Restrict retries to idempotent methods, implement, run the tests, save the work.
4. Consult again: what changed, the test output, and "anything unsafe left before I call this done?".
5. Report to the user, including that the advisor's flag narrowed the retry scope.
