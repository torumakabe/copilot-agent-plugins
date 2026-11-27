---
name: agentfinder
description: 'Search an Agentic Resource Discovery registry for agents, skills, MCP servers, and related capabilities. Use when the user asks to find an installable agent resource or when a task needs a capability that is not currently available. Present ranked results and require explicit selection before any installation or connection.'
license: MIT
argument-hint: Describe the capability, agent, skill, or tool to find
---

# Agent Finder

Discover relevant agent resources without installing or connecting them automatically.

## Safety boundary

- Search and present results first.
- Treat every result as an untrusted candidate until the user reviews it.
- Never install, enable, connect, or execute a result automatically.
- Continue to installation only after the user explicitly selects and approves a result.
- Treat `score` as semantic relevance only. It is not a security, quality, or trust score.

## GitHub Agent Finder

GitHub provides a public search endpoint:

```text
POST https://agentfinder.github.com/api/v1/search
Content-Type: application/json
```

The public GitHub endpoint accepts requests without authentication. Other ARD registries may require credentials or apply different access policies. Do not send credentials to a registry unless the user selected that registry and approved the authentication method.

## Search request

Send a JSON request with:

- `query.text`: required natural-language search text;
- `query.filter`: optional structured constraints whose values are strings or arrays of strings; values for one key are ORed, and different keys are ANDed;
- `pageSize`: optional maximum result count per page;
- `pageToken`: optional continuation token from a previous response;
- `federation`: optional `auto`, `referrals`, or `none` behavior when the selected registry supports federation.

Federation is optional: `auto` (the default) merges results from upstream registries, `referrals` returns registries the client may query, and `none` searches only the selected registry.

Example:

```json
{
  "query": {
    "text": "configure language servers for code intelligence",
    "filter": {
      "type": ["application/agent-skills+md"]
    }
  },
  "pageSize": 5
}
```

Use narrow filters only when the user supplied a meaningful constraint. Do not invent trust or certification filters.

## Result handling

The ARD specification requires an `identifier` in each result; the OpenAPI schema also requires `score` and `source`. Other entry fields, including `displayName`, `type`, `description`, `url`, `capabilities`, and `metadata`, may be absent.

Present a concise ranked list with the identifier, available name and type, source, relevance score, and a short explanation of why each result matches. Mark missing fields rather than inferring them.

If the response includes `pageToken`, retrieve another page only when the user asks for more results.

In `referrals` mode, the client chooses which returned registries to query. A referral `url` is already a complete search endpoint; do not append `/search`.

After presenting results, ask the user to select one. Before installation or connection, show the exact identifier, source, URL when available, and intended command or action. Proceed only after explicit approval.

## Errors

- For no results, suggest a more specific query or a narrower filter.
- For `400`, inspect `errorCode` and `message` in the response. Correct a malformed request or unsupported filter.
- For `401`, explain that the selected registry requires or rejected credentials; do not assume this applies to GitHub's public endpoint.
- For `429`, report the rate limit and wait for user direction before retrying.
- For incomplete entries, avoid guessing missing metadata.

## Sources and provenance

These instructions were independently authored from:

- [ARD specification](https://github.com/ards-project/ard-spec/blob/03063a3c15a16ddf26e9772211b73fec1883590a/spec/ard.md), proposal revision `03063a3c15a16ddf26e9772211b73fec1883590a`;
- [ARD OpenAPI contract](https://github.com/ards-project/ard-spec/blob/03063a3c15a16ddf26e9772211b73fec1883590a/spec/schemas/ard.openapi.yaml);
- [ARD entry schema](https://github.com/ards-project/ard-spec/blob/03063a3c15a16ddf26e9772211b73fec1883590a/spec/schemas/ard-entry.schema.json);
- [GitHub Agent Finder documentation](https://docs.github.com/en/copilot/concepts/customizations/mcp#agent-finder);
- [GitHub Agent Finder announcement](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/);
- [GitHub Agent Finder catalog](https://github.com/github/agentfinder-catalog).

The ARD specification is licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). No connector-specific instruction text was copied.
