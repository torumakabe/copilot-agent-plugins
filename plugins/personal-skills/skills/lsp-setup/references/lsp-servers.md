# Known LSP Servers for Copilot CLI

This reference lists common language servers, supported installation approaches, and configuration objects to merge under the top-level `lspServers` key.

The snippets assume that Copilot CLI starts from the repository root. For project-local Node.js packages, they use `npx --no-install` so the command cannot download a missing package at runtime. Adapt the launcher to the repository's existing package manager when needed.

## TypeScript and JavaScript

**Server**: [typescript-language-server](https://github.com/typescript-language-server/typescript-language-server)

Install `typescript` and `typescript-language-server` as development dependencies with the repository's existing Node.js package manager:

```shell
npm install --save-dev typescript typescript-language-server
```

Equivalent project-local `pnpm add --save-dev` or `yarn add --dev` commands are suitable when the repository already uses those package managers. An existing mise-managed installation is also suitable.

```json
{
  "typescript": {
    "command": "npx",
    "args": ["--no-install", "typescript-language-server", "--stdio"],
    "fileExtensions": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact",
      ".mts": "typescript",
      ".cts": "typescript",
      ".mjs": "javascript",
      ".cjs": "javascript"
    }
  }
}
```

## Java

**Server**: [Eclipse JDT Language Server](https://github.com/eclipse-jdtls/eclipse.jdt.ls)

JDT LS requires the Java version documented by its current release. Install it through Homebrew or an available distribution package, use an existing mise setup, or download an official milestone archive. Add the provided `jdtls` launcher to `PATH`; do not create a machine-specific wrapper in the repository.

```json
{
  "java": {
    "command": "jdtls",
    "args": [],
    "fileExtensions": {
      ".java": "java"
    }
  }
}
```

The `jdtls` launcher handles transport arguments. A manual archive installation may require a different command; follow the [JDT LS command-line documentation](https://github.com/eclipse-jdtls/eclipse.jdt.ls#running-from-the-command-line).

## Python

**Server**: [Pyright](https://github.com/microsoft/pyright)

Install `pyright` as a development dependency with the repository's existing Node.js package manager:

```shell
npm install --save-dev pyright
```

An existing mise-managed Pyright installation is also suitable. If the repository uses a Python-distributed language server instead, install and invoke it through `uv`; do not run the Python package installer directly.

```json
{
  "python": {
    "command": "npx",
    "args": ["--no-install", "pyright-langserver", "--stdio"],
    "fileExtensions": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}
```

## Go

**Server**: [gopls](https://pkg.go.dev/golang.org/x/tools/gopls)

Use an existing Go toolchain, a system package, Homebrew, or an existing mise setup. The Go toolchain can install the official server:

```shell
go install golang.org/x/tools/gopls@latest
```

Ensure the Go binary directory is already on the environment's `PATH`.

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "fileExtensions": {
      ".go": "go"
    }
  }
}
```

## Rust

**Server**: [rust-analyzer](https://github.com/rust-lang/rust-analyzer)

Prefer the component bundled for the repository's Rust toolchain:

```shell
rustup component add rust-analyzer
```

Distribution packages, Homebrew, an existing mise setup, and official release binaries are alternatives.

```json
{
  "rust": {
    "command": "rust-analyzer",
    "args": [],
    "fileExtensions": {
      ".rs": "rust"
    }
  }
}
```

## C and C++

**Server**: [clangd](https://clangd.llvm.org/)

Install LLVM or clangd through the operating-system package manager, Homebrew, an existing mise setup, Visual Studio tooling, or an [official LLVM release](https://releases.llvm.org/). Confirm that `clangd` resolves in the environment that launches Copilot CLI.

```json
{
  "cpp": {
    "command": "clangd",
    "args": ["--background-index"],
    "fileExtensions": {
      ".c": "c",
      ".h": "c",
      ".cpp": "cpp",
      ".cxx": "cpp",
      ".cc": "cpp",
      ".hpp": "cpp",
      ".hxx": "cpp"
    }
  }
}
```

Projects that use headers as C++ may map `.h` to `cpp` instead.

## C# and .NET

**Server**: [Roslyn Language Server](https://github.com/dotnet/roslyn)

Install the .NET SDK through the operating-system package manager, an existing mise setup, Visual Studio, or the official [.NET download](https://dotnet.microsoft.com/download). The following command uses the SDK's `dnx` support:

```json
{
  "csharp": {
    "command": "dotnet",
    "args": [
      "dnx",
      "roslyn-language-server",
      "--yes",
      "--prerelease",
      "--",
      "--stdio",
      "--autoLoadProjects"
    ],
    "fileExtensions": {
      ".cs": "csharp"
    }
  }
}
```

Confirm that the installed SDK supports `dotnet dnx`. If it does not, use the Roslyn distribution supported by the project's SDK rather than changing the SDK solely for LSP setup.

## Ruby

**Server**: [Solargraph](https://github.com/castwide/solargraph)

Add Solargraph to the repository's bundle:

```shell
bundle add solargraph --group development
```

Use the repository's existing Ruby toolchain or mise setup.

```json
{
  "ruby": {
    "command": "bundle",
    "args": ["exec", "solargraph", "stdio"],
    "fileExtensions": {
      ".rb": "ruby",
      ".rake": "ruby",
      ".gemspec": "ruby"
    }
  }
}
```

## PHP

**Server**: [Intelephense](https://github.com/bmewburn/vscode-intelephense)

Install `intelephense` as a development dependency with the repository's existing Node.js package manager:

```shell
npm install --save-dev intelephense
```

```json
{
  "php": {
    "command": "npx",
    "args": ["--no-install", "intelephense", "--stdio"],
    "fileExtensions": {
      ".php": "php"
    }
  }
}
```

## Kotlin

**Server**: [kotlin-language-server](https://github.com/fwcd/kotlin-language-server)

Use Homebrew, an available operating-system package, an existing mise setup, or an official release archive. Add the release's launcher to `PATH`.

```json
{
  "kotlin": {
    "command": "kotlin-language-server",
    "args": [],
    "fileExtensions": {
      ".kt": "kotlin",
      ".kts": "kotlin"
    }
  }
}
```

## Swift

**Server**: [SourceKit-LSP](https://github.com/swiftlang/sourcekit-lsp)

SourceKit-LSP is bundled with the Swift toolchain. Install Swift through Xcode, the official Swift toolchain, an operating-system package, or an existing mise setup.

On macOS, use `xcrun` so the active Xcode toolchain selects the executable:

```json
{
  "swift": {
    "command": "xcrun",
    "args": ["sourcekit-lsp"],
    "fileExtensions": {
      ".swift": "swift"
    }
  }
}
```

On Linux or Windows, when `sourcekit-lsp` is already on `PATH`, use `"command": "sourcekit-lsp"` and an empty `args` array.

## Lua

**Server**: [Lua Language Server](https://github.com/LuaLS/lua-language-server)

Use Homebrew, an available operating-system package, an existing mise setup, or an [official release](https://github.com/LuaLS/lua-language-server/releases). Add the release executable to `PATH`.

```json
{
  "lua": {
    "command": "lua-language-server",
    "args": [],
    "fileExtensions": {
      ".lua": "lua"
    }
  }
}
```

## YAML

**Server**: [yaml-language-server](https://github.com/redhat-developer/yaml-language-server)

Install `yaml-language-server` as a development dependency with the repository's existing Node.js package manager:

```shell
npm install --save-dev yaml-language-server
```

```json
{
  "yaml": {
    "command": "npx",
    "args": ["--no-install", "yaml-language-server", "--stdio"],
    "fileExtensions": {
      ".yaml": "yaml",
      ".yml": "yaml"
    }
  }
}
```

## Bash and shell scripts

**Server**: [Bash Language Server](https://github.com/bash-lsp/bash-language-server)

Install `bash-language-server` as a development dependency with the repository's existing Node.js package manager:

```shell
npm install --save-dev bash-language-server
```

```json
{
  "bash": {
    "command": "npx",
    "args": ["--no-install", "bash-language-server", "start"],
    "fileExtensions": {
      ".sh": "shellscript",
      ".bash": "shellscript",
      ".zsh": "shellscript"
    }
  }
}
```

## Adapting a snippet

Before merging a snippet:

1. Confirm the server's current installation instructions from its official documentation.
2. Match the repository's existing package manager and tool-version policy.
3. Replace the launcher only when the selected installation method requires it.
4. Read and merge the existing LSP JSON without removing unrelated configuration.
5. Verify the executable with `command -v` on POSIX or `Get-Command` on Windows.
