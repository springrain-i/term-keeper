#!/usr/bin/env python3
"""Render a default Markdown project glossary into a review-friendly HTML table."""

from __future__ import annotations

import argparse
import html
import re
from datetime import date
from pathlib import Path


FIELD_LABELS = {
    "type": "Type",
    "类型": "Type",
    "definition": "Definition",
    "定义": "Definition",
    "source": "Source / owner",
    "source / owner": "Source / owner",
    "来源": "Source / owner",
    "来源 / 维护": "Source / owner",
    "maintenance rule": "Maintenance rule",
    "maintenance/update rule": "Maintenance rule",
    "维护规则": "Maintenance rule",
    "boundary": "Boundary / deprecated meaning",
    "boundary / anti-example": "Boundary / deprecated meaning",
    "deprecated meaning": "Boundary / deprecated meaning",
    "边界": "Boundary / deprecated meaning",
    "边界 / 反例": "Boundary / deprecated meaning",
    "废弃含义": "Boundary / deprecated meaning",
    "confirmation status": "Confirmation status",
    "确认状态": "Confirmation status",
    "last modified": "Last modified",
    "last modified date": "Last modified",
    "最后修改": "Last modified",
    "最后修改日期": "Last modified",
    "trigger frequency": "Trigger frequency",
    "usage frequency": "Trigger frequency",
    "触发频率": "Trigger frequency",
    "使用频率": "Trigger frequency",
}

COLUMNS = [
    "术语",
    "类型",
    "定义",
    "来源 / 负责人",
    "维护规则",
    "边界 / 废弃含义",
    "最后修改",
    "触发频率",
    "确认状态",
]

INTERNAL_TO_DISPLAY = {
    "Term": "术语",
    "Type": "类型",
    "Definition": "定义",
    "Source / owner": "来源 / 负责人",
    "Maintenance rule": "维护规则",
    "Boundary / deprecated meaning": "边界 / 废弃含义",
    "Last modified": "最后修改",
    "Trigger frequency": "触发频率",
    "Confirmation status": "确认状态",
}


def parse_entries(markdown: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", markdown, re.M))
    for index, match in enumerate(matches):
        term = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        block = markdown[start:end]
        entry = {column: "" for column in COLUMNS}
        entry["术语"] = term
        loose_lines: list[str] = []
        for line in block.splitlines():
            bullet = re.match(r"^\s*[-*]\s*([^:：]+)\s*[:：]\s*(.*?)\s*$", line)
            if bullet:
                raw_key = bullet.group(1).strip().lower()
                value = bullet.group(2).strip()
                column = FIELD_LABELS.get(raw_key)
                if column:
                    entry[INTERNAL_TO_DISPLAY[column]] = value
                else:
                    loose_lines.append(line.strip())
            elif line.strip() and not line.lstrip().startswith("#"):
                loose_lines.append(line.strip())
        if loose_lines and not entry["定义"]:
            entry["定义"] = " ".join(loose_lines)
        entries.append(entry)
    return entries


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def render_html(entries: list[dict[str, str]], title: str) -> str:
    rows = []
    today = date.today().isoformat()
    for entry in entries:
        entry["最后修改"] = entry.get("最后修改") or today
        entry["触发频率"] = entry.get("触发频率") or "0"
        entry["确认状态"] = entry.get("确认状态") or "待确认"
        for optional_text_field in ["类型", "定义", "来源 / 负责人", "维护规则", "边界 / 废弃含义"]:
            entry[optional_text_field] = entry.get(optional_text_field) or "未记录"

    for entry in entries:
        cells = []
        for index, column in enumerate(COLUMNS):
            value = esc(entry.get(column, ""))
            if index == 0:
                cells.append(f'<td class="term">{value}</td>')
            elif column == "类型":
                cells.append(f'<td><span class="tag">{value}</span></td>')
            elif column == "确认状态":
                raw_status = entry.get(column, "")
                raw_status_lower = raw_status.lower()
                status_class = "pending" if "待确认" in raw_status or "need" in raw_status_lower or "pending" in raw_status_lower else "confirmed"
                display_value = "待确认" if status_class == "pending" else "已确认"
                cells.append(f'<td><span class="status {status_class}">{display_value}</span></td>')
            elif column == "触发频率":
                cells.append(f'<td><span class="frequency">{value}</span></td>')
            else:
                cells.append(f"<td>{value}</td>")
        rows.append(f"        <tr>{''.join(cells)}</tr>")
    header = "".join(f"<th>{esc(column)}</th>" for column in COLUMNS)
    total = len(entries)
    confirmed = sum(1 for entry in entries if "已确认" in entry.get("确认状态", "") or "confirm" in entry.get("确认状态", "").lower())
    pending = sum(1 for entry in entries if "待确认" in entry.get("确认状态", "") or "need" in entry.get("确认状态", "").lower() or "pending" in entry.get("确认状态", "").lower())
    deprecated = sum(1 for entry in entries if "deprecated" in " ".join(entry.values()).lower() or "废弃" in " ".join(entry.values()))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=JetBrains+Mono:wght@400;500;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #1a1410;
      --ink-light: #3d3530;
      --ink-muted: #8a7f78;
      --accent: #c84b2f;
      --accent-light: #fdf0ed;
      --accent-2: #2b5c8a;
      --accent-2-light: #edf3f9;
      --accent-3: #2d7a4f;
      --accent-3-light: #edf7f2;
      --warn: #d4820a;
      --warn-light: #fdf5e6;
      --paper: #faf8f5;
      --paper-warm: #f5f0ea;
      --surface: #fffdfa;
      --border: #e8e0d8;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", Arial, sans-serif; line-height: 1.55; }}
    .page {{ max-width: 1440px; margin: 0 auto; padding: 28px 24px 42px; }}
    .doc-head {{ display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end; border-bottom: 2px solid var(--ink); padding-bottom: 16px; margin-bottom: 16px; }}
    .eyebrow {{ margin: 0 0 8px; font-family: "JetBrains Mono", monospace; font-size: 10px; letter-spacing: .28em; text-transform: uppercase; color: var(--accent); }}
    h1 {{ margin: 0; font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", SimSun, serif; font-size: 30px; line-height: 1.25; letter-spacing: 0; color: var(--ink); }}
    .subtitle {{ margin: 8px 0 0; max-width: 760px; color: var(--ink-muted); font-size: 13px; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, auto); gap: 14px; align-items: end; font-family: "JetBrains Mono", monospace; }}
    .summary-item {{ min-width: 72px; border-left: 2px solid var(--border); padding-left: 10px; }}
    .summary-item strong {{ display: block; color: var(--accent); font-size: 22px; line-height: 1; }}
    .summary-item span {{ display: block; margin-top: 5px; color: var(--ink-muted); font-size: 10px; letter-spacing: .08em; text-transform: uppercase; white-space: nowrap; }}
    .table-wrap {{ border: 1px solid var(--border); background: var(--surface); overflow: auto; }}
    table {{ width: 100%; min-width: 1232px; border-collapse: collapse; table-layout: fixed; font-size: 12px; }}
    col.term-col {{ width: 140px; }}
    col.type-col {{ width: 95px; }}
    col.definition-col {{ width: 225px; }}
    col.owner-col {{ width: 120px; }}
    col.rule-col {{ width: 155px; }}
    col.boundary-col {{ width: 235px; }}
    col.modified-col {{ width: 92px; }}
    col.frequency-col {{ width: 78px; }}
    col.status-col {{ width: 92px; }}
    thead th {{ position: sticky; top: 0; z-index: 2; background: var(--paper-warm); padding: 9px 12px; border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); color: var(--ink-muted); text-align: left; font-family: "JetBrains Mono", monospace; font-size: 10px; letter-spacing: .08em; font-weight: 500; white-space: nowrap; }}
    tbody td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); color: var(--ink-light); vertical-align: top; word-break: break-word; }}
    thead th:last-child, tbody td:last-child {{ border-right: 0; }}
    tbody tr:hover td {{ background: var(--paper-warm); }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    .term {{ width: 160px; color: var(--ink); font-weight: 700; }}
    .tag, .frequency, .status {{ display: inline-block; border-radius: 2px; padding: 2px 7px; font-family: "JetBrains Mono", monospace; font-size: 10px; font-weight: 500; white-space: nowrap; }}
    .tag {{ background: var(--accent-2-light); color: var(--accent-2); border: 1px solid #d5e4f1; }}
    .frequency {{ min-width: 34px; text-align: right; background: var(--paper-warm); color: var(--ink-light); border: 1px solid var(--border); }}
    .status.confirmed {{ background: var(--accent-3-light); color: var(--accent-3); border: 1px solid #d2e8da; }}
    .status.pending {{ background: var(--warn-light); color: var(--warn); border: 1px solid #efd7a8; }}
    .footnote {{ margin-top: 10px; border-left: 3px solid var(--accent); background: var(--paper-warm); padding: 9px 12px; color: var(--ink-muted); font-size: 12px; }}
    @media (max-width: 860px) {{
      .page {{ padding: 22px 14px 36px; }}
      .doc-head {{ display: block; }}
      h1 {{ font-size: 28px; }}
      .summary {{ grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 16px; }}
      table {{ min-width: 1080px; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header class="doc-head">
      <div>
        <p class="eyebrow">Glossary Table · Review Snapshot</p>
        <h1>{esc(title)}</h1>
        <p class="subtitle">表格用于审阅长期术语、角色边界、展示口径与废弃说法。写入前先确认定义，确认后同步 Markdown 与 HTML。</p>
      </div>
      <div class="summary" aria-label="summary">
        <div class="summary-item"><strong>{total}</strong><span>词条</span></div>
        <div class="summary-item"><strong>{confirmed}</strong><span>已确认</span></div>
        <div class="summary-item"><strong>{pending}</strong><span>待确认</span></div>
        <div class="summary-item"><strong>{deprecated}</strong><span>已废弃</span></div>
      </div>
    </header>
    <section class="table-wrap" aria-label="glossary table">
      <table>
        <colgroup>
          <col class="term-col" />
          <col class="type-col" />
          <col class="definition-col" />
          <col class="owner-col" />
          <col class="rule-col" />
          <col class="boundary-col" />
          <col class="modified-col" />
          <col class="frequency-col" />
          <col class="status-col" />
        </colgroup>
        <thead><tr>{header}</tr></thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </section>
    <p class="footnote">维护规则：先生成确认表，使用者确认后再写入 Markdown，并同步生成 HTML 表格审阅版。</p>
  </div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Markdown glossary headings into an HTML review table.")
    parser.add_argument("--md", required=True, help="Input Markdown glossary path")
    parser.add_argument("--html", required=True, help="Output HTML review path")
    parser.add_argument("--title", default="Project Glossary", help="HTML page title")
    args = parser.parse_args()

    md_path = Path(args.md)
    html_path = Path(args.html)
    markdown = md_path.read_text(encoding="utf-8-sig")
    entries = parse_entries(markdown)
    if not entries:
        raise SystemExit("No glossary entries found. Use ## Term headings in the Markdown glossary.")
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(entries, args.title), encoding="utf-8")
    print(f"Rendered {len(entries)} entries to {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
