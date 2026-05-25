---
name: term-keeper
description: Use when a user explicitly defines, corrects, renames, deprecates, or clarifies durable project concepts, glossary terms, domain vocabulary, module meanings, agent or role boundaries, dashboard/reporting semantics, pipeline terms, data-source meanings, or says to remember a project definition or wording rule.
---

# Term Keeper

## Purpose

Maintain a durable project term dictionary or glossary for any project. Record long-lived semantics, boundaries, and wording rules that future agents or contributors should reuse. Treat the user's explicit definitions as the highest-authority source.

This skill is not tied to one repository, language, framework, or project path. For project-specific paths and rules, first look for a local dictionary config or ask the user for the dictionary files.

## Locate the Dictionary

1. Use dictionary paths explicitly provided by the user first.
2. If paths are not provided, look for a nearby project config such as `project_dictionary_config.md`, `.project-dictionary.md`, `docs/glossary.md`, `docs/glossary.html`, `docs/project_glossary.md`, `docs/project_design_dictionary.md`, or `docs/project_design_dictionary.html`.
3. Prefer an existing project-local dictionary over creating a new file.
4. If no dictionary exists and the user clearly asks to record a durable definition, use `docs/glossary.md` as the default Markdown dictionary path and `docs/glossary.html` as the default user-review HTML path unless a local config says otherwise.
5. Maintain a user-review HTML dictionary alongside the Markdown dictionary by default. If an existing project config explicitly disables HTML output, follow the project config and mention that no HTML was updated.
6. If multiple candidates exist, choose the one closest to the current workspace and mention the assumption.
7. Ask for a path only when there is no safe default or creating `docs/glossary.md` would be inappropriate for the workspace.
8. For a reusable config template, see `references/dictionary-config-template.md`.

## Trigger Decision

Use this skill when the user is making a durable vocabulary decision, for example:

- "以后 X 指的是..."
- "这个概念改成..."
- "记住这个口径..."
- "X 不是 Y"
- "废弃这个说法..."
- "这个模块/Agent/角色的边界是..."

Do not update the dictionary for:

- Current run status, batch progress, temporary errors, today's result, or one-off execution notes.
- Your own interpretation, architectural preference, or inferred naming.
- Implementation details that do not change durable meaning or boundary.
- Vague discussion where the user has not confirmed the definition.

If the user asks what a term means, read the dictionary and answer; do not edit unless they define or correct the term.

Use this quick decision table:

| User intent | Action |
| --- | --- |
| Defines, corrects, renames, or deprecates a durable concept | Draft a confirmation table before updating |
| Mentions or uses an existing dictionary term without changing its meaning | Increment trigger frequency only |
| Asks what a term means | Read and answer only |
| Describes a current run, batch, incident, or temporary state | Do not update |
| Gives an ambiguous idea that would affect roles, workflow, reporting, or data sources | Ask before updating |
| Says "maybe", "consider", "could be", or asks for your opinion | Do not record as user definition |

## Classification

Before editing, classify each change into one or more of these categories:

- Term definition: stable meaning of a name or phrase.
- Module meaning: what a module/view/document represents.
- Agent or role boundary: what an agent/role owns, must not do, or hands off.
- Dashboard or reporting semantics: what a displayed metric, table, tab, or status means.
- Pipeline semantics: what a workflow step, transition, artifact, or notification means.
- Data-source or sync semantics: canonical source, fallback, update rule, or ownership.
- Deprecated meaning: wording or interpretation that is no longer current.

If a concept does not fit any category, add it only after the user confirms that it belongs in the dictionary.

## Write Rules

1. Read the current dictionary files before editing.
2. Extract only candidate definitions, corrections, boundaries, and deprecations that came from the user.
3. Before editing definition-bearing fields, show the user a confirmation table and ask whether the proposed wording is accurate.
4. Do not write definition-bearing changes to the dictionary until the user explicitly approves the table or provides corrected wording.
5. Preserve the user's approved wording where practical, especially business terms and role names.
6. Keep each entry useful for future agents:
   - Type/category.
   - Definition.
   - Source or owner.
   - Maintenance or update rule.
   - Boundary, anti-example, or deprecated meaning.
   - Last modified date.
   - Trigger frequency, if the project has a cheap local source for it.
   - Confirmation status when useful.
7. Update the Markdown dictionary and user-review HTML dictionary directly in the same turn after approval. The agent is responsible for keeping both files synchronized; scripts are optional helpers, not a requirement for routine maintenance.
8. Mark obsolete meanings as deprecated instead of silently deleting them when they may prevent future confusion.
9. If the change affects agent responsibilities, workflow order, production pipeline behavior, external reporting, dashboard semantics, or canonical data sources, call that impact out in the confirmation table before writing.

Trigger frequency is metadata, not a definition change:

- Increment `触发频率` by 1 when the user mentions an existing dictionary term in a relevant project context.
- Increment `触发频率` by 1 when the agent explicitly uses an existing dictionary term to interpret, route, validate, or update project work.
- Do not scan full chat history, full repository history, reports, or the web to recompute frequency unless the user explicitly asks.
- Do not increment for accidental text matches, code identifiers, unrelated examples, or generated table/header text.
- If only `触发频率` changes, no confirmation table is required and no routine output is needed; the updated value is visible in the Markdown and HTML dictionaries.
- Trigger-frequency-only updates must still update every canonical dictionary format, including the HTML review table. Prefer direct synchronized edits. If a project explicitly treats HTML as generated output, update Markdown first and then use the renderer.
- If a term is new, confirm and write the term first, then initialize `触发频率` to 1.

Use this confirmation table before every definition-bearing write:

| Term | Type | Proposed definition | Boundary / deprecated meaning | Source wording | Impact | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Term name | Classification | User-confirmed wording to write | Anti-example, limit, or old meaning | Short excerpt/paraphrase from user | none / roles / workflow / reporting / data source | add / update / deprecate |

Ask: "请确认上表定义是否准确；确认后我再写入词典。"

If the user corrects the table, revise the table and ask again. If the user confirms only part of the table, write only the confirmed rows and leave the rest as pending.

Use this Markdown entry shape when starting a new dictionary:

```markdown
# Project Glossary

## Term

- Type:
- Definition:
- Source / owner:
- Maintenance rule:
- Boundary / anti-example:
- Deprecated meaning:
- Last modified:
- Trigger frequency:
- Confirmation status:
```

For existing dictionaries, preserve the project's current structure unless it blocks clear maintenance.

When maintaining the HTML review version:

- Keep it readable for non-technical reviewers.
- Use Chinese table headers by default: `术语`、`类型`、`定义`、`来源 / 负责人`、`维护规则`、`边界 / 废弃含义`、`最后修改`、`触发频率`、`确认状态`.
- Treat `触发频率` as incremental metadata. Update it from current user mentions or explicit agent use; do not perform expensive repository-wide, chat-history-wide, or web-wide scans just to calculate it unless the user asks for that analysis.
- Preserve an existing HTML structure if the project already has one.
- Default to direct synchronized edits for small or structure-preserving changes.
- Use the bundled renderer only when the project uses the default heading-and-bullet Markdown structure and regeneration is safer than manual HTML editing. The renderer is optional, not a daily dependency:

```bash
python scripts/render_glossary_html.py --md path/to/glossary.md --html path/to/glossary.html
```

## Guardrails

- Do not invent missing definitions.
- Do not convert current status into long-term semantics.
- Do not use old memory or prior chat over the current dictionary when they conflict.
- Do not let examples become rules unless the user says they are rules.
- Do not replace the user's definition with a cleaner-sounding abstraction.
- Do not update only one dictionary version when multiple canonical versions exist.
- Do not take over orchestration, product decisions, UI implementation, or pipeline execution; this skill only maintains the dictionary.

Runtime/status words are red flags, not automatic blockers: current, latest, today, this batch, run, running, temporary, test batch, 当前, 最新, 今天, 本轮, 当前批次, 运行中, 临时, 测试批次. When these appear, decide whether the user is defining a durable semantic boundary or only reporting a transient state.

## Verification

After editing:

1. Check that every changed term exists in every canonical dictionary version.
2. Check that Markdown headings and HTML/table rows represent the same term set when both formats exist.
3. Check that required fields are not empty.
4. Check that deprecated meanings are visible in every maintained format.
5. Check that runtime/status language was not written as a long-term definition.
6. If `触发频率` changed, check that the same value appears in the HTML review table.

If a Python runtime is available, use the bundled read-only checker as an optional verification helper. This is useful for release checks, CI, and risky edits, but does not replace the agent's responsibility to inspect both dictionary formats:

```bash
python scripts/check_dictionary_sync.py --md path/to/glossary.md
python scripts/check_dictionary_sync.py --md path/to/project_design_dictionary.md --html path/to/project_design_dictionary.html
```

For forward testing this skill, use `references/pressure-test-scenarios.md`.

## Output

After a maintenance run, report:

- Terms changed.
- Dictionary files updated.
- Classification for each changed term.
- Verification result.
- Any user confirmation still needed.

Do not include trigger-frequency-only increments in routine output unless the user asks to see them.

If no edit was made, state why: no explicit definition, transient status only, missing dictionary path, or confirmation required.
