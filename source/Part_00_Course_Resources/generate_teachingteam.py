#!/usr/bin/env python3
"""
Generate Section Information HTML from a CSV.
"""

from __future__ import annotations

import csv
import html
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List

# CONFIGURATION
SEMESTER_NAME = "Fall 2026"
CSV_INPUT = Path("source/Part_00_Course_Resources/teaching_team/sections.csv")
OUTPUT_HTML = Path("source/Part_00_Course_Resources/teaching_team/sections.html")


@dataclass
class Section:
    section_num: str
    rm_location: str
    days: str
    time: str
    instructor_name: str
    instructor_email: str
    gta_name: str
    gta_email: str

    def sort_key(self):
        # Numeric sections first, then strings
        try:
            return (0, int(self.section_num))
        except ValueError:
            return (1, self.section_num)


def read_sections(csv_path: Path) -> List[Section]:
    sections = []
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found.")
        return []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sections.append(
                Section(
                    section_num=(row.get("section_num") or "").strip(),
                    rm_location=(row.get("rm_location") or "TBD").strip(),
                    days=(row.get("days") or "TBD").strip(),
                    time=(row.get("time") or "TBD").strip(),
                    instructor_name=(row.get("instructor_name") or "TBD").strip(),
                    instructor_email=(row.get("instructor_email") or "").strip(),
                    gta_name=(row.get("gta_name") or "TBD").strip(),
                    gta_email=(row.get("gta_email") or "").strip(),
                )
            )
    return sorted(sections, key=lambda s: s.sort_key())


def build_html(sections: List[Section]) -> str:
    # 1. Define the CSS - Simplified for better platform compatibility
    css = """
<style>
  :root {
    --sch-text: #1f2937;
    --sch-border: #d1d5db;
    --sch-card-bg: #ffffff;
    --sch-accent: #1a73e8;
    --sch-label: #4b5563;
    --sch-datetime:
  }

  /* Dark mode scheme from the scheduling script */
  html[data-theme="dark"] {
    --sch-text: #f3f4f6;           /* Main text */
    --sch-border: #374151;         /* Subtle borders */
    --sch-card-bg: #1b2430;        /* Slightly lighter card surface */
    --sch-accent: #8ab4f8;         /* High-contrast links */
    --sch-label: #CACFD3;          /* Muted labels */
  }

  /* Optional: Also trigger on system settings for local testing */
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --sch-text: #f3f4f6;
      --sch-border: #374151;
      --sch-card-bg: #1b2430;
      --sch-accent: #8ab4f8;
      --sch-label: #CACFD3;
    }
  }

  body {
    color: var(--sch-text);
    font-family: 'Segoe UI', Roboto, sans-serif;
    margin: 2rem;
  }

  .staff-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .staff-card {
    background: var(--sch-card-bg);
    border: 1px solid var(--sch-border);
    border-radius: 8px;
    padding: 1.25rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .staff-card h3 {
    margin: 0 0 0.75rem 0;
    border-bottom: 2px solid var(--sch-accent);
    padding-bottom: 0.5rem;
    font-size: 1.2rem;
    font-weight: 600px;
    color: var(--sch-text);
  }

  .staff-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: bold;
    color: var(--sch-label);
    margin-top: 1rem;
    display: block;
  }

  .staff-name {
    font-weight: 600;
    display: block;
  }

  .staff-email {
    font-size: 0.85rem;
    display: block;
  }

  .staff-email a {
    color: var(--sch-accent);
    text-decoration: none;
  }

  .staff-email a:hover {
    text-decoration: underline;
  }
</style>
"""

    cards_html = []
    for s in sections:

        def format_email(email):
            if not email or "@" not in email:
                return ""
            # Written-out hyperlinked email as requested
            return f'<span class="staff-email"><a href="mailto:{email}">{html.escape(email)}</a></span>'

        # CRITICAL: textwrap.dedent removes the leading spaces that cause the "gray box" code bug
        card = textwrap.dedent(f"""
        <div class="staff-card">
          <h3 style="font-weight: 700px;">Section {html.escape(s.section_num)}</h3>
          <div style="font-size: 1.1rem; color: --sch-label; margin-bottom: 1rem;">
            <strong>{html.escape(s.days)} {html.escape(s.time)}</strong><br>
            {html.escape(s.rm_location)}
          </div>
          <div class="staff-label">Instructor</div>
          <span class="staff-name">{html.escape(s.instructor_name)}</span>
          {format_email(s.instructor_email)}
          <div class="staff-label">GTA</div>
          <span class="staff-name">{html.escape(s.gta_name)}</span>
          {format_email(s.gta_email)}
        </div>""").strip()

        cards_html.append(card)

    header = f"<h2>ENGR 131: {html.escape(SEMESTER_NAME)} Section Information</h2>"

    # Returning as a single block with NO leading spaces
    return (
        css
        + header
        + '\n<div class="staff-grid">\n'
        + "\n".join(cards_html)
        + "\n</div>"
    )


def main() -> None:
    sections = read_sections(CSV_INPUT)
    html_content = build_html(sections)

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"Successfully generated {OUTPUT_HTML} with {len(sections)} sections.")


if __name__ == "__main__":
    main()
