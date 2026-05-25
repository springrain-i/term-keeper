# Installation

## Install Locally

Copy the bundled skill package into your Codex skills directory:

```text
repo-root/skill/term-keeper/ -> <codex-home>/skills/term-keeper/
```

The package should contain `SKILL.md` at its root.

## Add Project Configuration

For a project that already has dictionary files, create a project-local config by copying:

```text
skill/term-keeper/references/dictionary-config-template.md
```

Recommended project paths:

```text
docs/glossary.md
docs/glossary.html
```

Adjust the config if your project uses different paths.

## First Use

Ask Codex to use the skill when you want to record a durable definition:

```text
Use term-keeper.
以后 "Review HTML" 指给使用者审阅词表的 HTML 表格版，和 Markdown 词表保持同步。
```

The agent should ask for confirmation before writing definition-bearing changes.

## Notes

- Do not use the skill as a runtime log.
- Do not ask it to replace your project controller, scheduler, or UI implementation.
- Use it for durable semantics and boundaries.
