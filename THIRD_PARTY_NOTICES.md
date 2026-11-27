# Third-party notices

## Japanese technical writing

`plugins/personal-skills/skills/japanese-technical-writing/SKILL.md` is adapted for Copilot plugin packaging from:

- source Gist revision [`c7189cdc9c2520be50418209834145bdf3a46e97`](https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d/c7189cdc9c2520be50418209834145bdf3a46e97);
- raw `SKILL.md` revision [`9f6709de186a5d8cfc7557ab6f0befb6664cf598`](https://gist.githubusercontent.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d/raw/9f6709de186a5d8cfc7557ab6f0befb6664cf598/SKILL.md);
- public Unlicense declaration at Gist [`67625f2a7d96e3bbdfae8d571a936063`](https://gist.github.com/k16shikano/67625f2a7d96e3bbdfae8d571a936063/1092e6b60296c760071c308624e344469ec345cf), revision `1092e6b60296c760071c308624e344469ec345cf`.

The packaged copy adds Agent Skills license metadata and retains the Copilot CLI adaptation. It is distributed under the Unlicense.

## Agentic Resource Discovery

`plugins/personal-skills/skills/agentfinder/SKILL.md` was independently authored from the ARD specification text, OpenAPI and entry contracts at revision [`03063a3c15a16ddf26e9772211b73fec1883590a`](https://github.com/ards-project/ard-spec/tree/03063a3c15a16ddf26e9772211b73fec1883590a), which are licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

The ARD contracts are referenced as technical sources. No ARD connector instruction text was copied.

## Awesome GitHub Copilot LSP Setup

`plugins/personal-skills/skills/lsp-setup/` is copied verbatim from [`github/awesome-copilot`](https://github.com/github/awesome-copilot/tree/1d6704fed9b4ac9e1666a5a6c70d84c410a55aff/skills/lsp-setup) at commit `1d6704fed9b4ac9e1666a5a6c70d84c410a55aff`.

```text
MIT License

Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Anthropic skill creator

`plugins/skill-creator/skills/skill-creator/SKILL.md` selectively adapts Anthropic's [`skills/skill-creator/SKILL.md`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/skill-creator/SKILL.md) at commit `3b3fad96af16a10759d930941b4520ba0c40edae`.

Copyright 2026 Anthropic, PBC. The upstream work and this adapted skill are distributed under Apache License 2.0. The unchanged upstream license is included at `plugins/skill-creator/skills/skill-creator/LICENSE.txt`.

The adaptation retains guidance for intent capture, skill anatomy, progressive disclosure, predictable behavior, writing patterns, and lean improvement. It replaces the Claude-oriented lifecycle with GitHub Copilot authoring, the repository-pinned official `skills-ref` validator, an independently authored deterministic ZIP packager, and local Copilot discovery commands. The packaging script is distributed with the adapted skill under Apache License 2.0. The adaptation omits the upstream evaluation and benchmark workflow, grader/comparator/analyzer agents, description optimization, subprocess orchestration, JSON artifacts, reports, and HTML review tooling.
