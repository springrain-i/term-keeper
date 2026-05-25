#!/usr/bin/env python3
"""Read-only project glossary/dictionary checker."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


RUNTIME_WORDS = [
    "current",
    "latest",
    "today",
    "this batch",
    "running",
    "temporary",
    "test batch",
    "当前",
    "最新",
    "今天",
    "本轮",
    "当前批次",
    "运行中",
    "临时",
    "测试批次",
]

FIELD_LABELS = {
    "last modified": "最后修改",
    "last modified date": "最后修改",
    "最后修改": "最后修改",
    "最后修改日期": "最后修改",
    "trigger frequency": "触发频率",
    "usage frequency": "触发频率",
    "触发频率": "触发频率",
    "使用频率": "触发频率",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def markdown_heading_terms(text: str) -> list[str]:
    terms: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            terms.append(match.group(1).strip())
    return terms


def markdown_table_terms(text: str) -> list[str]:
    terms: list[str] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        header = cells[0].lower()
        if header not in {"term", "name", "术语", "名词", "概念"}:
            continue
        if index + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-{3,}:?\s*\|", lines[index + 1]):
            continue
        for row in lines[index + 2 :]:
            if "|" not in row:
                break
            row_cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if row_cells and row_cells[0]:
                terms.append(row_cells[0])
    return terms


def markdown_terms(text: str) -> list[str]:
    terms = markdown_heading_terms(text)
    if terms:
        return terms
    return markdown_table_terms(text)


def markdown_heading_entries(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    for index, match in enumerate(matches):
        term = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        fields: dict[str, str] = {}
        for line in block.splitlines():
            bullet = re.match(r"^\s*[-*]\s*([^:：]+)\s*[:：]\s*(.*?)\s*$", line)
            if not bullet:
                continue
            key = bullet.group(1).strip().lower()
            value = bullet.group(2).strip()
            normalized = FIELD_LABELS.get(key)
            if normalized:
                fields[normalized] = value
        entries[term] = fields
    return entries


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def html_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for row_match in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", text, re.I | re.S):
        row = row_match.group(1)
        cells = [strip_tags(cell.group(1)) for cell in re.finditer(r"<td\b[^>]*>(.*?)</td>", row, re.I | re.S)]
        if cells:
            rows.append(cells)
    return rows


def html_headers(text: str) -> list[str]:
    match = re.search(r"<thead\b[^>]*>(.*?)</thead>", text, re.I | re.S)
    if not match:
        return []
    return [strip_tags(cell.group(1)) for cell in re.finditer(r"<th\b[^>]*>(.*?)</th>", match.group(1), re.I | re.S)]


def report_missing(label: str, values: list[str]) -> int:
    if not values:
        return 0
    print(f"{label}:")
    for value in values:
        print(f"  - {value}")
    return len(values)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project glossary/dictionary structure and optional HTML synchronization.")
    parser.add_argument("--md", required=True, help="Markdown dictionary path")
    parser.add_argument("--html", help="Optional HTML dictionary path")
    args = parser.parse_args()

    md_path = Path(args.md)
    md_text = read_text(md_path)

    md_terms = markdown_terms(md_text)
    if not md_terms:
        print("FAILED: no Markdown terms found. Use ## Term headings or a Markdown table whose first column is Term/Name/术语/名词/概念.")
        return 1

    problems = 0
    html_terms: list[str] = []

    if args.html:
        html_path = Path(args.html)
        html_text = read_text(html_path)
        rows = html_rows(html_text)
        headers = html_headers(html_text)
        html_terms = [row[0] for row in rows if row]

        problems += report_missing("Only in Markdown", [term for term in md_terms if term not in html_terms])
        problems += report_missing("Only in HTML", [term for term in html_terms if term not in md_terms])

        empty_rows = []
        optional_empty_headers = {"最后修改", "触发频率", "Last modified", "Trigger frequency"}
        for row in rows:
            has_required_empty = False
            for index, cell in enumerate(row):
                header = headers[index] if index < len(headers) else ""
                if not cell and header not in optional_empty_headers:
                    has_required_empty = True
                    break
            if has_required_empty:
                empty_rows.append(row[0] if row else "(unknown row)")
        problems += report_missing("Rows with empty cells", empty_rows)

        markdown_fields = markdown_heading_entries(md_text)
        html_by_term = {row[0]: row for row in rows if row}
        field_mismatches = []
        for term, fields in markdown_fields.items():
            row = html_by_term.get(term)
            if not row:
                continue
            for field_name in ["最后修改", "触发频率"]:
                expected = fields.get(field_name)
                if expected is None or field_name not in headers:
                    continue
                index = headers.index(field_name)
                actual = row[index] if index < len(row) else ""
                if actual != expected:
                    field_mismatches.append(f"{term} / {field_name}: Markdown={expected} HTML={actual}")
        problems += report_missing("Field mismatches", field_mismatches)

    runtime_hits = []
    for term in md_terms:
        term_pattern = re.compile(rf"^##\s+{re.escape(term)}\s*$([\s\S]*?)(?=^##\s+|\Z)", re.M)
        match = term_pattern.search(md_text)
        block = match.group(0) if match else ""
        if any(word.lower() in block.lower() for word in RUNTIME_WORDS):
            runtime_hits.append(term)
    if runtime_hits:
        print("Runtime/status language found; manually verify these are durable semantics:")
        for term in runtime_hits:
            print(f"  - {term}")

    if problems:
        print(f"FAILED: {problems} synchronization problem(s) found.")
        return 1

    if args.html:
        print(f"OK: {len(md_terms)} Markdown terms and {len(html_terms)} HTML terms are synchronized.")
    else:
        print(f"OK: {len(md_terms)} Markdown terms found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
