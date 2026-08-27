---
name: skill-creator
description: 'Create or update Agent Skills for GitHub Copilot. Use when the user wants to turn a workflow into a SKILL.md, revise an existing skill, organize scripts or references, validate skill metadata, package a skill as a ZIP archive, or verify local Copilot discovery.'
license: Apache-2.0
---

# Skill Creator

> **Modification notice:** This file adapts Anthropic's `skill-creator` from commit `3b3fad96af16a10759d930941b4520ba0c40edae`. It was changed for GitHub Copilot CLI and reduced to the intent, authoring, validation, packaging, and local discovery workflow documented below.

Create skills whose behavior matches their descriptions and whose instructions remain concise enough to load only when useful.

## Workflow

1. Understand the intended workflow and trigger.
2. Inspect an existing skill or create the minimal directory structure.
3. Write or revise `SKILL.md` and only the supporting resources the workflow needs.
4. Validate the skill with the official `skills-ref` implementation.
5. Package the skill when a distributable archive is needed.
6. Load it locally with GitHub Copilot CLI and verify discovery.
7. Review the result once more and remove instructions or files that do not improve the workflow.

## Capture intent

Use the current conversation and available files before asking questions. Extract:

- what the skill enables Copilot to do;
- when it should trigger;
- the expected output or side effect;
- the sequence of tools and decisions;
- corrections, edge cases, and constraints already supplied by the user;
- inputs, outputs, dependencies, and source-of-truth files.

Ask only for gaps that materially affect the skill. Confirm the intended trigger and output before creating a new skill when the answer is not already clear.

The `description` frontmatter is the primary trigger. State both what the skill does and the situations in which it should be used. Do not hide trigger conditions only in the body.

## Inspect or create the skill

An Agent Skill uses this structure:

```text
skill-name/
├── SKILL.md
├── scripts/       optional deterministic or repetitive operations
├── references/    optional documentation loaded when needed
└── assets/        optional templates or files used in outputs
```

Before editing, inspect the complete skill directory and repository instructions. Preserve existing behavior and user-authored content unless the requested change requires otherwise.

Create only directories that have content. Do not add empty placeholders or extra process documents.

## Apply progressive disclosure

Skills load information in three stages:

1. `name` and `description` metadata are always available for discovery.
2. The `SKILL.md` body loads when the skill is selected.
3. Bundled resources load or execute only when the instructions reference them.

Keep the main workflow in `SKILL.md`. Move stable detail into `references/` when it would distract from the workflow. Put deterministic repeated operations in `scripts/`, and output templates or reusable files in `assets/`.

Aim to keep `SKILL.md` below 500 lines. When a reference exceeds about 300 lines, add a table of contents. Link each resource from `SKILL.md` and state when to read or run it.

Do not duplicate the same guidance in the body and a reference file.

## Write predictable instructions

A skill should not surprise the user. Its description, instructions, tools, network access, file changes, and other side effects must describe the same intent.

- Do not add hidden installation, network, credential, destructive, or persistence behavior.
- Do not create misleading instructions or facilitate unauthorized access or data extraction.
- Respect repository instructions and configuration ownership.
- Surface required approval before an irreversible or externally visible action.

Prefer imperative instructions. Explain why a constraint matters instead of relying on repeated absolute wording.

Use concrete output templates when structure must be exact:

```markdown
## Output format

# [Title]

## Summary

## Findings
```

Use examples when they clarify an ambiguous input, decision, or output. Keep examples representative rather than making the skill specific to one sample.

Match the level of freedom to the task. Use prose for judgment calls and a script for operations that must be repeatable. After drafting, read the skill with fresh context and remove duplication, ineffective instructions, and unnecessary files.

## Validate with the pinned official tool

This repository pins `skills-ref` and its dependencies in `requirements.txt`. From the repository root, create the validation environment and install the locked tools:

```shell
uv venv
uv pip sync requirements.txt --require-hashes
```

Run the official validator on the skill directory:

```shell
.venv/bin/agentskills validate path/to/skill
```

On Windows:

```powershell
.\.venv\Scripts\agentskills.exe validate path\to\skill
```

If the skill uses documented Copilot-only frontmatter that the pinned `skills-ref` release does not yet recognize, use the repository's existing validation adapter rather than weakening the skill or reimplementing frontmatter rules.

Resolve validation errors in `SKILL.md` before packaging. The packaging script intentionally does not parse YAML or invoke the validator.

## Package the skill

Run the bundled stdlib-only PEP 723 script with `uv`:

```shell
uv run --script <skill-creator-directory>/scripts/package_skill.py \
  path/to/skill \
  --output dist/skill-name.zip
```

Use `--force` only when replacing an existing archive is intentional. The script requires an exact-case regular `SKILL.md`, writes deterministic sorted entries under the skill directory name, rejects output inside the source, and excludes symlinks and routine junk.

Inspect the resulting archive and confirm that every path begins with the skill directory name.

## Verify local Copilot discovery

Use disposable `COPILOT_HOME` and `COPILOT_CACHE_HOME` directories so development checks do not modify the user's normal Copilot state.

Install a local plugin directory by absolute path:

```shell
copilot plugin install /absolute/path/to/plugin
copilot plugin list
copilot skill list --json
```

Register a local directory that contains one or more skill subdirectories:

```shell
copilot skill add /absolute/path/to/skills-directory
copilot skill list --json
```

For a local marketplace repository:

```shell
copilot plugin marketplace add /absolute/path/to/repository
copilot plugin install plugin-name@marketplace-name
copilot plugin list
copilot skill list --json
```

Verify the expected skill name, source, and enabled state. When the local marketplace uses a live directory source, start a new Copilot session or restart the current one after edits.

## Improve leanly

Use observed user corrections and actual workflow friction to refine the skill. Generalize from repeated needs, not hypothetical complexity.

- Tighten the description when discovery intent is unclear.
- Add a reference only when the body has stable detail that is not always needed.
- Add a script only when repetition or determinism justifies code.
- Remove instructions that do not change agent behavior.
- Stop when another revision would not produce a meaningful improvement.

## License

The adapted source and modifications in this skill directory are distributed under Apache License 2.0. See [LICENSE.txt](LICENSE.txt).
