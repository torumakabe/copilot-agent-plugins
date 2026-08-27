# Copilot Agent Plugins

This repository is the public Agent Plugins marketplace maintained by `torumakabe`.

The marketplace contains two plugins:

| Plugin | Contents |
| --- | --- |
| `personal-skills` | `agentfinder`, `japanese-technical-writing`, and `lsp-setup` |
| `skill-creator` | Create, validate, package, and locally verify Agent Skills |

## Layout

```text
.github/plugin/marketplace.json  Marketplace catalog
plugins/<name>/plugin.json       Agent Plugins 1.0 manifest
plugins/<name>/skills/           Agent Skills included by a plugin
scripts/validate-marketplace.mjs Marketplace and manifest consistency
```

Skills belong under `plugins/<name>/skills/<skill>/SKILL.md`. Their metadata is validated by the official `skills-ref` implementation, so repository tooling does not duplicate Agent Skills frontmatter rules. Documented Copilot extensions such as `argument-hint` remain available to skill authors.

## Install

```shell
copilot plugin marketplace add torumakabe/copilot-agent-plugins
copilot plugin install personal-skills@torumakabe-agent-plugins
copilot plugin install skill-creator@torumakabe-agent-plugins
```

The installed skills become available to Copilot when their descriptions match a task. `agentfinder` supports direct invocation with a capability description, and `skill-creator` handles requests to create or revise an Agent Skill.

## Validation

CI runs on pull requests and pushes to `main` with read-only permissions. It:

1. validates each manifest with the official Agent Plugins 1.0 schema;
2. checks that marketplace sources exist and that names and versions match their manifests;
3. runs the focused standard-library tests for the skill packaging script;
4. runs `skills-ref` validation for every included skill.

Marketplace consistency can be checked locally with:

```shell
npm ci
npm run validate
```

## Owner workflow

`main` is the source used for normal plugin updates. Before changing it, the owner:

1. reviews the exact diff and commit;
2. reviews the CI result;
3. uses disposable `COPILOT_HOME` and `COPILOT_CACHE_HOME` directories for a real Copilot CLI smoke test against `torumakabe/copilot-agent-plugins#branch`;
4. manually merges or pushes the validated change.

For example, in PowerShell:

```powershell
$env:COPILOT_HOME = Join-Path $env:TEMP "copilot-agent-plugins-smoke-home"
$env:COPILOT_CACHE_HOME = Join-Path $env:TEMP "copilot-agent-plugins-smoke-cache"
copilot plugin marketplace add torumakabe/copilot-agent-plugins#my-branch
copilot plugin install personal-skills@torumakabe-agent-plugins
copilot plugin list
```

Installed caches, authentication material, and runtime state remain outside source control.

If a bad version reaches `main`, publish a higher-version forward fix. For an urgent stop, disable the affected plugin in the applicable desired-state configuration rather than decreasing its version.

## License

Original work in this repository is licensed under the [MIT License](LICENSE). Imported or derived material must retain its own license and notices; add third-party notices when such content is introduced.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the Japanese writing source and the ARD specification used to author `agentfinder`.
