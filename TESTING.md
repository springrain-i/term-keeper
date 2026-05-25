# Minimal Testing

The skill is designed so the agent can maintain Markdown and HTML directly. The scripts below are optional checks for release, CI, or risky edits.

## Validate Skill Shape

Use the Codex skill validator if available:

```bash
python <codex-home>/skills/.system/skill-creator/scripts/quick_validate.py skill/term-keeper
```

On Windows with Chinese text, prefer UTF-8 mode:

```powershell
$env:PYTHONUTF8='1'
python <codex-home>\skills\.system\skill-creator\scripts\quick_validate.py skill\term-keeper
```

## Render a Minimal Glossary

Create a small Markdown file:

```markdown
# Project Glossary

## Agent Router

- Type: Agent or role boundary
- Definition: Classifies requests and hands them off to the correct agent.
- Source / owner: User confirmed
- Maintenance rule: Responsibility changes require confirmation.
- Boundary / anti-example: Not a scheduler.
- Deprecated meaning:
- Last modified: 2026-01-15
- Trigger frequency: 1
- Confirmation status: confirmed
```

Render HTML:

```bash
python skill/term-keeper/scripts/render_glossary_html.py --md docs/glossary.md --html docs/glossary.html --title "Project Glossary"
```

## Check Markdown and HTML Sync

```bash
python skill/term-keeper/scripts/check_dictionary_sync.py --md docs/glossary.md --html docs/glossary.html
```

Expected result:

```text
OK: 1 Markdown terms and 1 HTML terms are synchronized.
```

## Release Checklist

- `SKILL.md` validates.
- No local absolute paths remain in the skill package.
- No `__pycache__`, `.pyc`, temporary screenshots, or personal project files remain.
- Demo HTML opens locally.
- Markdown and HTML examples stay synchronized.
