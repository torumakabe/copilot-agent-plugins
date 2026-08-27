---
name: lsp-setup
description: 'Enable code intelligence such as go-to-definition, find-references, hover, and type information for GitHub Copilot CLI by installing and configuring an LSP server. Use when code intelligence is unavailable or when the user asks to set up, install, or configure an LSP server. Supports repository-level and user-level configuration while preserving existing settings and dotfile ownership.'
license: MIT
---

# LSP Setup for GitHub Copilot CLI

Install and configure Language Server Protocol servers for GitHub Copilot CLI.

Use this skill for requests to set up an LSP server, enable code intelligence, or diagnose a missing LSP configuration. Do not use it for editor-specific configuration or ordinary coding tasks where an LSP server already works.

## Workflow

1. Determine the requested language from the user request and repository contents. Ask only when the language remains ambiguous.
2. Detect the operating system. On POSIX, use `uname -s`; on Windows, inspect `$env:OS`.
3. Inspect the repository instructions, manifests, lockfiles, tool-version configuration, and existing LSP files before choosing an installation method.
4. Read [references/lsp-servers.md](references/lsp-servers.md) for the server and a configuration snippet.
5. Prefer repository-level configuration. Reuse `lsp.json` or `.github/lsp.json` when either exists; otherwise choose one location consistent with repository conventions.
6. Install the server without introducing an unrelated package manager or version policy.
7. Read the selected JSON file if it exists, parse it, and merge the target server into `lspServers`. Preserve all unrelated keys and server entries.
8. Verify that the JSON parses and that the configured command resolves.
9. Restart Copilot CLI and use `/lsp` to confirm that the server starts in a repository containing matching files.

## Installation policy

Choose the first method that fits the repository and the server:

1. an existing project-local package manager and dependency manifest;
2. mise, only when the project or user already manages tools with mise;
3. an operating-system or language toolchain package manager already in use;
4. an official server release or toolchain bundle.

Follow these constraints:

- Never run `pip` directly. Use `uv add`, `uv tool install`, `uv pip install`, or `uv run` as appropriate.
- Never install Node.js language servers with `npm install -g`. Add them as project development dependencies, or use an existing mise setup.
- Do not add device-specific mise pins, installation scripts, or generated configuration templates.
- Do not change a repository's package manager solely to install an LSP server.
- Confirm commands on POSIX with `command -v <binary>`, not `which`. On Windows, use `Get-Command <binary>` or `where.exe <binary>`.

## Configuration locations and ownership

Copilot CLI reads LSP configuration from:

- repository level: `lsp.json` or `.github/lsp.json`;
- user level: `~/.copilot/lsp-config.json`.

Prefer repository-level configuration because it can be reviewed with the code and shared by contributors. If the user explicitly requests the user-level file, first determine whether a dotfile manager owns it. Update the manager's source of truth when it is available and in scope. If it is unavailable or outside the allowed edit scope, clearly report the required source change. Never overwrite a generated `~/.copilot/lsp-config.json` directly.

Before every write:

1. read the entire existing JSON file;
2. preserve top-level properties other than the intended change;
3. preserve unrelated `lspServers` entries;
4. add or update only the selected server key;
5. serialize valid JSON and review the resulting diff.

Never replace an existing configuration with a snippet from the reference file. The snippets are merge inputs, not complete-file replacements.

## Configuration format

```json
{
  "lspServers": {
    "<server-key>": {
      "command": "<binary>",
      "args": ["--stdio"],
      "fileExtensions": {
        ".<ext>": "<languageId>"
      }
    }
  }
}
```

- `command` is a binary on `PATH`, an absolute path, or a project-local launcher.
- `args` selects the server's standard-I/O transport when the server requires an explicit argument.
- `fileExtensions` maps extensions, including the leading dot, to [Language IDs](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers).
- Multiple servers can coexist under `lspServers`.

## Verification

Validate both configuration and runtime prerequisites:

1. Parse the final JSON with a JSON-aware tool.
2. Resolve the configured executable from the same environment that launches Copilot CLI.
3. If a project-local launcher is used, run it from the repository root and confirm that dependencies are installed.
4. Exit and relaunch Copilot CLI so it reloads the configuration.
5. Run `/lsp`, then try hover or go-to-definition on a matching source file.

If the server fails, report the command, observed output, configuration path, and operating system. Do not claim the setup works until `/lsp` or an equivalent server-start check succeeds.
