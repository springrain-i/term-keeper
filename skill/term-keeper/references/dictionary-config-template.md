# Project Dictionary Config Template

Use this file as a project-local adapter for `term-keeper`.

## Canonical Files

- Primary Markdown dictionary: `docs/glossary.md`
- User-review HTML dictionary: `docs/glossary.html`
- Optional synchronized outputs:

If the project already has a glossary or design dictionary, replace the default path with the existing file path.

## Entry Model

Each dictionary entry should include:

- Term:
- Type: term definition | module meaning | agent boundary | dashboard/reporting semantics | pipeline semantics | data-source/sync semantics | deprecated meaning
- Definition:
- Source or owner:
- Maintenance/update rule:
- Boundary or anti-example:
- Deprecated meaning:
- Last modified:
- Trigger frequency:
- Confirmation status: confirmed | needs user confirmation

## Project-Specific Confirmation Gates

Ask the user before writing changes that affect:

- Agent or role responsibilities:
- Workflow or pipeline order:
- Dashboard/reporting data sources:
- External-facing wording:
- Deprecated or renamed concepts:

## Default Write Policy

- Create `docs/glossary.md` and `docs/glossary.html` when the user clearly asks to record a durable definition and no dictionary exists.
- Present a confirmation table before every dictionary write.
- Write only after the user explicitly approves the proposed wording or provides corrected wording.
- Definition-bearing writes require confirmation. Trigger-frequency-only increments may be written without a confirmation table.
- Increment trigger frequency only from current user mentions or explicit agent use; do not scan full history unless requested.
- Trigger-frequency-only increments still update all canonical outputs, including the HTML review dictionary.
- Preserve the existing dictionary structure when one exists.
- Maintain the HTML review dictionary by default. Disable it only if the project explicitly does not want an HTML review output.
- The agent maintains Markdown and HTML directly by default. Scripts are optional helpers for rendering, checking, tests, or CI.
- Use an HTML renderer only when this project treats the HTML file as generated output.
- Maintain other table/wiki outputs only when this config marks them canonical.
- Keep examples separate from rules unless the user confirms the example is a rule.

## Runtime-State Red Flags

Do not record these as durable concepts unless the user explicitly says they are long-term semantics:

- Current run/status words:
- Temporary batch/test labels:
- One-off incident names:
- Today's/latest result:

## Local Notes

Add project-specific vocabulary, forbidden interpretations, and known dictionary locations here.
