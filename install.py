#!/usr/bin/env python3
"""Copy the advisor skill into a coding agent's skills directory.

Usage:
    python install.py --host agents              # ~/.agents/skills (read by most agents)
    python install.py --host claude              # ~/.claude/skills
    python install.py --host cursor --project    # ./.cursor/skills in the current project
    python install.py --host claude --dir PATH   # any other skills directory
    python install.py --list

Stdlib only. Safe to re-run: replaces an existing advisor directory.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent / "skills" / "advisor"

# host: (user-level directory, project-level directory). Taken from each
# agent's own documentation in November 2026; see the table in README.md.
HOSTS = {
    "agents": ("~/.agents/skills", ".agents/skills"),
    "claude": ("~/.claude/skills", ".claude/skills"),
    "codex": ("~/.agents/skills", ".agents/skills"),
    "cursor": ("~/.cursor/skills", ".cursor/skills"),
    "copilot": ("~/.copilot/skills", ".github/skills"),
    "gemini": ("~/.gemini/skills", ".gemini/skills"),
    "antigravity": ("~/.gemini/config/skills", ".agents/skills"),
    "kimi": ("~/.kimi-code/skills", ".kimi-code/skills"),
    "qwen": ("~/.qwen/skills", ".qwen/skills"),
    "opencode": ("~/.config/opencode/skills", ".opencode/skills"),
    "codewhale": ("~/.codewhale/skills", ".codewhale/skills"),
    "devin": ("~/.config/devin/skills", ".agents/skills"),
    "windsurf": ("~/.config/devin/skills", ".devin/skills"),
    "cline": ("~/.cline/skills", ".cline/skills"),
    "roo": ("~/.roo/skills", ".roo/skills"),
    "kilo": ("~/.kilo/skills", ".kilo/skills"),
    "vibe": ("~/.vibe/skills", ".vibe/skills"),
    "junie": ("~/.junie/skills", ".junie/skills"),
    "kiro": ("~/.kiro/skills", ".kiro/skills"),
    "amp": ("~/.config/agents/skills", ".agents/skills"),
}


def user_dir(host: str) -> Path:
    # Devin and Windsurf keep user skills under %APPDATA% on Windows.
    if host in ("devin", "windsurf") and os.name == "nt" and os.environ.get("APPDATA"):
        return Path(os.environ["APPDATA"]) / "devin" / "skills"
    return Path(HOSTS[host][0]).expanduser()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", choices=sorted(HOSTS), help="Agent to install into.")
    parser.add_argument("--project", action="store_true",
                        help="Install into the current project instead of your user directory.")
    parser.add_argument("--dir", help="Explicit skills directory (overrides --host and --project).")
    parser.add_argument("--list", action="store_true", help="Print the known directories and exit.")
    args = parser.parse_args()

    if args.list:
        for host, (_, project) in sorted(HOSTS.items()):
            print(f"{host:12} user: {user_dir(host)}   project: {project}")
        return 0
    if not args.host and not args.dir:
        parser.error("pass --host or --dir (see --list)")
    if not SKILL.is_dir():
        print(f"skill not found at {SKILL}; run this script from the repository root.", file=sys.stderr)
        return 1

    if args.dir:
        root = Path(args.dir).expanduser()
    elif args.project:
        root = Path.cwd() / HOSTS[args.host][1]
    else:
        root = user_dir(args.host)

    dest = root / "advisor"
    root.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() or dest.is_file():
        dest.unlink()
    elif dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SKILL, dest, ignore=shutil.ignore_patterns("evals"))
    print(f"installed {dest}")
    print("next: start a new session in your agent so it picks up the skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
