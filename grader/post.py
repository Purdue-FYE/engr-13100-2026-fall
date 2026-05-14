import json
import os
from datetime import datetime, timedelta

import pytz
from pytz import timezone

from tests.test_config import DUE_DATE

# ---------------------------------------------------------------------------
# Plant survival scoring constants
# ---------------------------------------------------------------------------
#: Maximum points for the plant-survival test entry injected by post.py.
PLANT_MAX_SCORE: float = 100.0

#: Name of the JSON file written by the autograder simulation test.
PLANT_REPORT_FILE: str = "plant_report.json"


def format_timedelta(td):
    # Drop the milliseconds from the default formatting.
    return str(td).split(".")[0]


def get_submission_time(json_data):
    try:
        # Try to get the real submission time.
        with open("../submission_metadata.json") as fo:
            data = json.load(fo)
        sub_dt = datetime.fromisoformat(data["created_at"])
    except Exception:
        # If the real submission time is not available,
        # subtract the execution time from the current time
        # to find the time when the code was submitted.
        execution_time = float(json_data["execution_time"])
        now_dt = datetime.now(pytz.utc)
        sub_dt = now_dt - timedelta(seconds=execution_time)

    return sub_dt


def _inject_plant_survival_score(json_data: dict) -> None:
    """
    Read ``plant_report.json`` (if present) and inject a Gradescope test
    entry with partial credit based on sols survived.

    The test entry uses ``visibility: "visible"`` so students immediately see
    their score and the failure report.
    """
    # Locate the report file relative to the grader's working directory or CWD.
    search_paths = [
        PLANT_REPORT_FILE,
        os.path.join(os.path.dirname(__file__), PLANT_REPORT_FILE),
    ]
    report_path = None
    for path in search_paths:
        if os.path.isfile(path):
            report_path = path
            break

    if report_path is None:
        return  # No simulation test was run; skip silently.

    try:
        with open(report_path, encoding="utf-8") as fh:
            report = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return  # Corrupt or unreadable; skip gracefully.

    sols_survived: float = float(report.get("sols_survived", 0.0))
    target_sols: float = float(report.get("target_sols", 30.0))
    failure_report: str = report.get("failure_report", "No failure report available.")

    score = round(PLANT_MAX_SCORE * min(sols_survived / max(target_sols, 1.0), 1.0), 3)

    plant_test = {
        "name": "Martian Greenhouse — Plant Survival Score",
        "score": score,
        "max_score": PLANT_MAX_SCORE,
        "output": failure_report,
        "visibility": "visible",
    }

    # Prepend so it appears at the top of the Gradescope results.
    json_data["tests"].insert(0, plant_test)
    json_data["score"] = round(json_data.get("score", 0.0) + score, 3)


def post_processor(json_data):
    # Inject plant survival score first (runs unconditionally).
    _inject_plant_survival_score(json_data)

    # Skip late-penalty logic if no DUE_DATE configured.
    if not DUE_DATE:
        return

    total_score = json_data["score"]
    max_score = sum(test.get("max_score", 0) for test in json_data["tests"])

    late_penalty = 25  # 25% penalty per day

    # Load the due date assuming it is defined in Eastern time.  The should
    # work for Standard time or Daylight time as long as the due date is not
    # during the transition between the two times.
    eastern = timezone("US/Eastern")
    due_dt = eastern.localize(datetime.strptime(DUE_DATE, "%Y-%m-%d %I:%M %p"))
    sub_dt = get_submission_time(json_data)

    # Calculate the time before the due date.
    delta_t = due_dt - sub_dt

    # Calculate the time before end date.
    end_t = timedelta(days=1, hours=2)

    if delta_t >= timedelta():
        # On time
        time = format_timedelta(delta_t)
        score = 0
        max_score = 0
        output = f"Submission on time. Time until due: {time}."
    elif delta_t >= -end_t:
        # Within late submission period. Deduct late penatly for every day
        # submission is late (at most total score points).
        days_late = -delta_t.days
        penalty_percent = late_penalty / 100 * days_late
        penalty_points = round(penalty_percent * max_score, 3)
        score = max(-total_score, -penalty_points)
        max_score = 0
        time_late = format_timedelta(-delta_t)
        output = (
            f"Submission late by {time_late}. {penalty_percent:.1%} penalty applied."
        )
    else:
        # Late beyond grace period.
        # Deduct all earned points.
        score = -total_score
        max_score = 0
        output = "Late submission. Not for credit."

    submission_time_test = {
        "name": "Check submission time.",
        "score": score,
        "max_score": max_score,
        "output": output,
    }

    json_data["tests"].insert(0, submission_time_test)
    json_data["score"] = round(json_data["score"] + score, 3)
