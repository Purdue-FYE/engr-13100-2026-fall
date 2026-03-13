#!/usr/bin/env python3
"""
Generate ENGR 131 schedule HTML from an ordered topic list CSV.

What this script does:
- reads a simple `schedule_topics.csv` file with one column: `topic`
- auto-generates Weeks 1–16 with A/B class meetings
- auto-fills week date ranges from the Monday of Week 1
- blocks exam slots
- blocks Fall Break at 8A in fall
- blocks Thanksgiving week in fall
- blocks Spring Break slots in spring
- fits topics into the remaining instructional class slots in order
- writes a standalone HTML schedule file

Suggested repo locations:
- source/Part_00_Course_Resources/course_schedule/schedule_topics.csv
- source/Part_00_Course_Resources/course_schedule/generate_schedule.py
- source/Part_00_Course_Resources/course_schedule/student_course_schedule.html

Run:
    python source/Part_00_Course_Resources/course_schedule/generate_schedule.py
"""

from __future__ import annotations

import csv
import html
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List

# MAKE ALL CHANGES STARTING HERE
SEMESTER_NAME = "Fall 2026"
TERM = "fall"   # "fall" or "spring"
START_DATE = "2026-08-24"  # Monday of Week 1
WEEKS = 16

# Placeholder exam slots for now
EXAM_SLOTS = ["5A", "10A", "13A"]

# Fall Break is always Week 8 during class A; Spring Break is always 10A and 10B
FALL_BREAK_SLOT = "8A"
SPRING_BREAK_SLOTS = ["10A", "10B"]

""" 
DO NOT CHANGE ANYTHING BELOW THIS LINE
"""

# Input / output paths relative to repo root
TOPICS_CSV = Path("source/Part_00_Course_Resources/course_schedule/schedule_topics.csv")
ASSIGNMENTS_CSV = Path("source/Part_00_Course_Resources/course_schedule/schedule_assignments.csv")
OUTPUT_HTML = Path("source/Part_00_Course_Resources/course_schedule/student_course_schedule.html")

@dataclass
class ClassSlot:
    week: int
    meeting: str
    week_monday: date
    class_date: date
    topic: str = ""
    row_kind: str = "instruction"  # instruction, exam, fall_break, thanksgiving_break, spring_break

    @property
    def slot_id(self) -> str:
        return f"{self.week}{self.meeting}"

    @property
    def class_label(self) -> str:
        return f"Class {self.week}{self.meeting}"

    @property
    def week_label(self) -> str:
        friday = self.week_monday + timedelta(days=4)
        return f"Week {self.week} -- {format_month_day(self.week_monday)}-{format_month_day(friday)}"


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_month_day(d: date) -> str:
    return f"{d.month}/{d.day}"


def get_thanksgiving(year: int) -> date:
    nov1 = date(year, 11, 1)
    days_until_thursday = (3 - nov1.weekday()) % 7  # Monday=0, Thursday=3
    first_thursday = nov1 + timedelta(days=days_until_thursday)
    return first_thursday + timedelta(weeks=3)


def get_thanksgiving_week_monday(year: int) -> date:
    thanksgiving = get_thanksgiving(year)
    return thanksgiving - timedelta(days=thanksgiving.weekday())


def slot_date(week_monday: date, meeting: str) -> date:
    # Kept for future flexibility, even though class-specific dates are not displayed
    if meeting == "A":
        return week_monday + timedelta(days=1)  # Tuesday
    if meeting == "B":
        return week_monday + timedelta(days=3)  # Thursday
    raise ValueError("meeting must be 'A' or 'B'")


def read_topics(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Could not find topics file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("schedule_topics.csv is missing headers.")
        if "topic" not in reader.fieldnames:
            raise ValueError('schedule_topics.csv must contain a header named "topic".')

        topics: List[str] = []
        for row in reader:
            topic = (row.get("topic") or "").strip()
            if topic:
                topics.append(topic)

    return topics


def build_slots(start_monday: date, weeks: int) -> List[ClassSlot]:
    slots: List[ClassSlot] = []
    thanksgiving_week_monday = get_thanksgiving_week_monday(start_monday.year)

    for week in range(1, weeks + 1):
        week_monday = start_monday + timedelta(weeks=week - 1)
        for meeting in ("A", "B"):
            slot = ClassSlot(
                week=week,
                meeting=meeting,
                week_monday=week_monday,
                class_date=slot_date(week_monday, meeting),
            )

            if slot.slot_id in EXAM_SLOTS:
                slot.row_kind = "exam"
                slot.topic = "Exam"
            elif TERM.lower() == "fall" and slot.slot_id == FALL_BREAK_SLOT:
                slot.row_kind = "fall_break"
                slot.topic = "Fall Break"
            elif TERM.lower() == "fall" and week_monday == thanksgiving_week_monday:
                slot.row_kind = "thanksgiving_break"
                slot.topic = "Thanksgiving Break"
            elif TERM.lower() == "spring" and slot.slot_id in SPRING_BREAK_SLOTS:
                slot.row_kind = "spring_break"
                slot.topic = "Spring Break"

            slots.append(slot)

    return slots


def fill_topics(slots: List[ClassSlot], topics: List[str]) -> None:
    open_slots = [s for s in slots if s.row_kind == "instruction"]

    if len(topics) > len(open_slots):
        raise ValueError(
            f"There are {len(topics)} topics but only {len(open_slots)} open instructional slots. "
            "Reduce the topic list or adjust blocked slots."
        )

    for slot, topic in zip(open_slots, topics):
        slot.topic = topic


def build_html(slots: List[ClassSlot], assignments_by_slot) -> str:
    parts: List[str] = []

    styles = """
<style>
:root {
  --sch-col-1: 7rem;
  --sch-col-3: 4.5rem;
  --sch-col-4: 12rem;
  --sch-col-5: 8rem;

  --sch-text: #1f2937;
  --sch-border: #d1d5db;
  --sch-surface: #ffffff;

  --sch-exam-header-bg: transparent;
  --sch-exam-row-bg: #f8fbff;

  --sch-week-bg: transparent;
  --sch-week-text: #374151;

  --sch-class-bg: #e9eef4;
  --sch-class-text: #1f2937;

  --sch-break-bg: #fef3c7;
  --sch-break-text: #78350f;

  --sch-assignment-head-bg: #f7f8fa;
  --sch-assignment-head-text: #4b5563;

  --sch-assignment-body-bg: #ffffff;
  --sch-assignment-body-text: #1f2937;
}

html[data-theme="dark"] {
  --sch-text: #e5e7eb;
  --sch-border: #374151;
  --sch-surface: transparent;

  --sch-exam-header-bg: transparent;
  --sch-exam-row-bg: #111827;

  --sch-week-bg: transparent;
  --sch-week-text: #d1d5db;

  --sch-class-bg: #1b2430;
  --sch-class-text: #f3f4f6;

  --sch-break-bg: #3f2f12;
  --sch-break-text: #fef3c7;

  --sch-assignment-head-bg: #111827;
  --sch-assignment-head-text: #d1d5db;

  --sch-assignment-body-bg: #0b1220;
  --sch-assignment-body-text: #f3f4f6;

  .exam-slot-row td {
  background: #1e293b;
  color: #BBD9FC;
}
}

.schedule-wrap {
  max-width: 1100px;
  margin: 1.5rem auto;
  color: var(--sch-text);
}

.schedule-meta {
  margin-bottom: 0.75rem;
  font-size: 1.5rem;
}

.week-block {
  margin-bottom: 1rem;
}

.schedule-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.schedule-table td,
.schedule-table th {
  border: 1px solid var(--sch-border);
  padding: 0.6rem 0.75rem;
  text-align: left;
  vertical-align: top;
  color: inherit;
}

.schedule-table tr:hover td,
.schedule-table tr:hover th {
  background: inherit;
  color: inherit;
}

.exam-table {
  margin-bottom: 1.25rem;
}

.exam-header td {
  background: var(--sch-exam-header-bg);
  color: var(--sch-text);
  font-weight: 700;
  padding: 0.6rem 0.75rem 0.6rem 1rem;
  font-size: 1.2rem;
  border-left: none;
  border-right: none;
  border-top: none;
  border-bottom: 2px solid var(--sch-border);
  padding-left: 0.2rem;
}

.exam-row td {
  background: var(--sch-exam-row-bg);
  color: var(--sch-text);
}

.exam-row td:first-child {
  width: var(--sch-col-1);
  white-space: nowrap;
}

.week-label td {
  background: var(--sch-week-bg);
  color: var(--sch-week-text);
  font-weight: 700;
  font-size: 1.2rem; 
  padding: 0.55rem 0.25rem 0.55rem 1rem;
  border-left: none;
  border-right: none;
  border-top: none;
  border-bottom: 1px solid var(--sch-border);
  padding-left: 0.2rem;
}

.class-row td {
  background: var(--sch-class-bg);
  color: var(--sch-class-text);
  font-weight: 600;
}

.break-row td {
  background: var(--sch-break-bg);
  color: var(--sch-break-text);
  font-weight: 600;
}

/* ================================
   Exam rows inside weekly schedule
   ================================ */
.exam-slot-row td {
  background: #e6fffb;   /* very light turquoise */
  color: #0f766e;        /* teal text */
  font-weight: 600;
}

.assignment-head th {
  background: var(--sch-assignment-head-bg);
  color: var(--sch-assignment-head-text);
  font-weight: 600;
}

.assignment-body td {
  background: var(--sch-assignment-body-bg);
  color: var(--sch-assignment-body-text);
  white-space: normal;
  overflow-wrap: break-word;
  word-break: normal;
}

.nowrap {
  white-space: nowrap;
}

@media (max-width: 768px) {
  :root {
    --sch-col-1: 5.5rem;
    --sch-col-3: 3.5rem;
    --sch-col-4: 6.5rem;
    --sch-col-5: 5.5rem;
  }

  .schedule-table,
  .assignment-table {
    font-size: 0.82rem;
  }

  .schedule-table td,
  .schedule-table th,
  .assignment-table td,
  .assignment-table th {
    padding: 0.45rem 0.5rem;
  }

  .nowrap {
    white-space: normal;
  }
}

.schedule-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

</style>
""".strip()

    parts.append(styles)
    parts.append("")
    parts.append('<div class="schedule-wrap">')
    parts.append(f'  <div class="schedule-meta"><strong>Semester:</strong> {html.escape(SEMESTER_NAME)}</div>')

    # Exam schedule table
    parts.append('  <div class="schedule-scroll">')
    parts.append('  <table class="schedule-table exam-table">')
    parts.append('    <colgroup>')
    parts.append('      <col style="width: var(--sch-col-1)">')
    parts.append('      <col>')
    parts.append('    </colgroup>')
    parts.append('    <tbody>')
    parts.append('      <tr class="exam-header"><td colspan="2">Exam Schedule</td></tr>')
    for idx, slot_id in enumerate(EXAM_SLOTS, start=1):
        parts.append(
            f'      <tr class="exam-row"><td class="nowrap">Exam {idx}</td><td>In-Class Exam (Class {html.escape(slot_id)})</td></tr>'
        )
    parts.append('    </tbody>')
    parts.append('  </table>')
    parts.append('  </div>')

    # Group slots by week
    slots_by_week: dict[int, list[ClassSlot]] = {}
    for slot in slots:
        slots_by_week.setdefault(slot.week, []).append(slot)

    # One 5-column table per week
    for week_num in sorted(slots_by_week):
        week_slots = slots_by_week[week_num]
        week_label = week_slots[0].week_label

        parts.append('  <div class="week-block schedule-scroll">')
        parts.append('    <table class="schedule-table week-table">')
        parts.append('      <colgroup>')
        parts.append('        <col style="width: var(--sch-col-1)">')
        parts.append('        <col>')
        parts.append('        <col style="width: var(--sch-col-3)">')
        parts.append('        <col style="width: var(--sch-col-4)">')
        parts.append('        <col style="width: var(--sch-col-5)">')
        parts.append('      </colgroup>')
        parts.append('      <tbody>')
        parts.append(f'        <tr class="week-label"><td colspan="5">{html.escape(week_label)}</td></tr>')

        for slot in week_slots:
            if slot.row_kind == "exam":
                row_class = "exam-slot-row"
                topic = "Exam"
            elif slot.row_kind == "fall_break":
                row_class = "break-row"
                topic = "Fall Break"
            elif slot.row_kind == "thanksgiving_break":
                row_class = "break-row"
                topic = "Thanksgiving Break"
            elif slot.row_kind == "spring_break":
                row_class = "break-row"
                topic = "Spring Break"
            else:
                row_class = "class-row"
                topic = slot.topic

            # Class row spans cols 2-5
            parts.append(
                f'        <tr class="{row_class}"><td class="nowrap">{html.escape(slot.class_label)}</td><td colspan="4">{html.escape(topic)}</td></tr>'
            )

            assignments = assignments_by_slot.get(slot.slot_id, [])
            if assignments:
                parts.append('        <tr class="assignment-head">')
                parts.append('          <th>Assignment</th>')
                parts.append('          <th>Name</th>')
                parts.append('          <th>Points</th>')
                parts.append('          <th>Type</th>')
                parts.append('          <th>Due Date</th>')
                parts.append('        </tr>')

                for a in assignments:
                    parts.append(
                        f'        <tr class="assignment-body">'
                        f'<td class="nowrap">{html.escape(a["assignment_id"])}</td>'
                        f'<td>{html.escape(a["name"])}</td>'
                        f'<td class="nowrap">{html.escape(a["points"])}</td>'
                        f'<td>{html.escape(a["type"])}</td>'
                        f'<td>{html.escape(a["due_date"])}</td>'
                        f'</tr>'
                    )

        parts.append('      </tbody>')
        parts.append('    </table>')
        parts.append('  </div>')

    parts.append('</div>')

    return "\n".join(parts)

def read_assignments(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = ["class_slot", "assignment_id", "name", "points", "type", "due_date"]
        for col in required:
            if col not in (reader.fieldnames or []):
                raise ValueError(f'schedule_assignments.csv must contain a header named "{col}".')

        assignments_by_slot: dict[str, list[dict[str, str]]] = {}
        for row in reader:
            slot = (row.get("class_slot") or "").strip()
            if not slot:
                continue

            assignments_by_slot.setdefault(slot, []).append({
                "assignment_id": (row.get("assignment_id") or "").strip(),
                "name": (row.get("name") or "").strip(),
                "points": (row.get("points") or "").strip(),
                "type": (row.get("type") or "").strip(),
                "due_date": (row.get("due_date") or "").strip(),
            })

    return assignments_by_slot


def main() -> None:
    start_monday = parse_iso_date(START_DATE)
    if start_monday.weekday() != 0:
        raise ValueError("START_DATE must be the Monday of Week 1.")

    term_value = TERM.lower()
    if term_value not in {"fall", "spring"}:
        raise ValueError('TERM must be either "fall" or "spring".')

    topics = read_topics(TOPICS_CSV)
    assignments_by_slot = read_assignments(ASSIGNMENTS_CSV)
    slots = build_slots(start_monday, WEEKS)
    fill_topics(slots, topics)

    html_output = build_html(slots, assignments_by_slot)
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html_output, encoding="utf-8")

    open_instructional = sum(1 for s in slots if s.row_kind == "instruction")
    used_topics = sum(1 for s in slots if s.row_kind == "instruction" and s.topic)

    print(f"Wrote HTML schedule to: {OUTPUT_HTML}")
    print(f"Topics placed: {used_topics} / {open_instructional} open instructional slots")


if __name__ == "__main__":
    main()