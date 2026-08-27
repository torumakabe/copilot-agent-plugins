# Third-party notices

## Japanese technical writing

`plugins/personal-skills/skills/japanese-technical-writing/SKILL.md` is adapted for Copilot plugin packaging from:

- source Gist revision [`c7189cdc9c2520be50418209834145bdf3a46e97`](https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d/c7189cdc9c2520be50418209834145bdf3a46e97);
- raw `SKILL.md` revision [`9f6709de186a5d8cfc7557ab6f0befb6664cf598`](https://gist.githubusercontent.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d/raw/9f6709de186a5d8cfc7557ab6f0befb6664cf598/SKILL.md);
- public Unlicense declaration at Gist [`67625f2a7d96e3bbdfae8d571a936063`](https://gist.github.com/k16shikano/67625f2a7d96e3bbdfae8d571a936063/1092e6b60296c760071c308624e344469ec345cf), revision `1092e6b60296c760071c308624e344469ec345cf`.

The packaged copy adds Agent Skills license metadata and retains the Copilot CLI adaptation. It is distributed under the Unlicense.

## Agentic Resource Discovery

`plugins/personal-skills/skills/agentfinder/SKILL.md` was independently authored from the ARD OpenAPI and entry contracts at revision [`c21ac6a70c5ee0c857a84db875a81e44a028919d`](https://github.com/ards-project/ard-spec/tree/c21ac6a70c5ee0c857a84db875a81e44a028919d), which are licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

The ARD contracts are referenced as normative technical sources. No ARD connector instruction text was copied.

## Anthropic skill creator

`plugins/skill-creator/skills/skill-creator/SKILL.md` selectively adapts Anthropic's [`skills/skill-creator/SKILL.md`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/skill-creator/SKILL.md) at commit `3b3fad96af16a10759d930941b4520ba0c40edae`.

Copyright 2026 Anthropic, PBC. The upstream work and this adapted skill are distributed under Apache License 2.0. The unchanged upstream license is included at `plugins/skill-creator/skills/skill-creator/LICENSE.txt`.

The adaptation retains guidance for intent capture, skill anatomy, progressive disclosure, predictable behavior, writing patterns, and lean improvement. It replaces the Claude-oriented lifecycle with GitHub Copilot authoring, the repository-pinned official `skills-ref` validator, an independently authored deterministic ZIP packager, and local Copilot discovery commands. The packaging script is distributed with the adapted skill under Apache License 2.0. The adaptation omits the upstream evaluation and benchmark workflow, grader/comparator/analyzer agents, description optimization, subprocess orchestration, JSON artifacts, reports, and HTML review tooling.
