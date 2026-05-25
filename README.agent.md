# Term Keeper Agent Readme

This file is for AI agents reading this repository quickly. The canonical installable skill is `skill/term-keeper/SKILL.md`.

## Purpose

Use `term-keeper` to maintain durable project vocabulary: glossary terms, domain concepts, module meanings, agent or role boundaries, dashboard/reporting semantics, pipeline terms, data-source meanings, and deprecated wording.

Do not use it as a runtime log, task scheduler, product owner, UI builder, or orchestration agent.

## Installable Package

```text
skill/term-keeper/
```

Copy that directory into the Codex skills directory as:

```text
<codex-home>/skills/term-keeper/
```

## Visual Demo Assets

- GitHub README screenshots: `screenshots/demo-glossary-table.png`, `screenshots/confirmation-table-flow.png`
- GitHub Pages source: `docs/index.html`
- GitHub Pages HTML demo: `docs/demo-glossary.html`
- Pages URL after enabling Pages: `https://springrain-i.github.io/term-keeper/`

## Default Dictionary Files

If a project has no local dictionary config, use:

```text
docs/glossary.md
docs/glossary.html
```

Markdown is agent-readable. HTML is the human-review table.

## Trigger Rules

Trigger when the user explicitly:

- Defines a durable term.
- Corrects a term.
- Renames or deprecates a term.
- Clarifies a module meaning.
- Clarifies an agent, role, dashboard, report, pipeline, or data-source boundary.
- Says to remember a project definition or wording rule.

Do not write when the user only describes:

- Current run state.
- Temporary batch progress.
- Today's result.
- A one-off incident.
- Your own inferred architecture or wording preference.

## Confirmation Gate

Before definition-bearing writes, show a confirmation table and wait for user approval.

Required confirmation table columns:

```text
Term | Type | Proposed definition | Boundary / deprecated meaning | Source wording | Impact | Action
```

Only write confirmed rows. If the user corrects the wording, revise the table and ask again.

## Maintenance Rules

- Preserve user-approved wording where practical.
- Maintain Markdown and HTML in the same turn.
- Agent may edit both files directly.
- Optional scripts are helpers only, not required for routine maintenance.
- Do not let examples become rules unless the user confirms that they are rules.
- Do not turn transient status into durable semantics.
- If a change affects agent responsibilities, workflow order, production pipeline behavior, dashboard semantics, reporting, or canonical data sources, call out that impact before writing.

## Trigger Frequency

`触发频率` is incremental metadata:

- Add 1 when the user mentions an existing dictionary term in relevant project context.
- Add 1 when the agent explicitly uses an existing term to interpret, route, validate, or update project work.
- Do not scan full chat history or repository history to recompute it unless requested.
- Frequency-only updates do not need a confirmation table and should not be routinely reported.

## Optional Scripts

Render default Markdown to HTML:

```bash
python skill/term-keeper/scripts/render_glossary_html.py --md docs/glossary.md --html docs/glossary.html
```

Check sync:

```bash
python skill/term-keeper/scripts/check_dictionary_sync.py --md docs/glossary.md --html docs/glossary.html
```

On Windows with Chinese text, prefer UTF-8 mode:

```powershell
$env:PYTHONUTF8='1'
```

## Verification Before Completion

After edits, verify:

- Changed terms exist in every canonical dictionary file.
- Markdown and HTML contain the same changed terms.
- Required fields are not empty.
- Deprecated meanings remain visible.
- Runtime/status words were not written as long-term definitions.
- If `触发频率` changed, the same value appears in HTML.
