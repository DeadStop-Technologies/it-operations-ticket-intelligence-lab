"""
Analyze IT ticket data and generate an executive summary.

Input:
- data/sample_tickets.csv

Output:
- reports/summary.md
"""

from pathlib import Path
from collections import Counter, defaultdict
import csv
import statistics

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "sample_tickets.csv"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def read_tickets() -> list[dict]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Missing data/sample_tickets.csv. Run: python src/generate_sample_data.py"
        )

    with DATA_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        row["sla_hours"] = int(row["sla_hours"])
        row["resolution_hours"] = float(row["resolution_hours"])
        row["first_response_hours"] = float(row["first_response_hours"])

    return rows


def percent(value: int, total: int) -> str:
    return f"{value / total:.1%}" if total else "0.0%"


def group_average(rows: list[dict], group_key: str, metric_key: str) -> dict[str, float]:
    grouped = defaultdict(list)

    for row in rows:
        grouped[row[group_key]].append(row[metric_key])

    return {key: statistics.mean(values) for key, values in grouped.items()}


def write_summary(rows: list[dict]) -> None:
    total = len(rows)
    resolved_rows = [r for r in rows if r["status"] in ["Resolved", "Closed"]]

    sla_met_count = sum(1 for r in rows if r["sla_met"] == "Yes")
    escalated_count = sum(1 for r in rows if r["escalated"] == "Yes")
    avg_resolution = statistics.mean([r["resolution_hours"] for r in resolved_rows])
    avg_first_response = statistics.mean([r["first_response_hours"] for r in rows])

    category_counts = Counter(r["category"] for r in rows)
    root_cause_counts = Counter(r["root_cause"] for r in rows)
    priority_counts = Counter(r["priority"] for r in rows)
    avg_resolution_by_priority = group_average(rows, "priority", "resolution_hours")

    summary = f"""# Ticket Intelligence Summary

This report is generated from synthetic IT operations ticket data.

## Executive Summary

- Total tickets analyzed: **{total}**
- Resolved or closed tickets: **{len(resolved_rows)}**
- SLA success rate: **{percent(sla_met_count, total)}**
- Escalation rate: **{percent(escalated_count, total)}**
- Average resolution time: **{avg_resolution:.2f} hours**
- Average first response time: **{avg_first_response:.2f} hours**

## Ticket Volume by Priority

| Priority | Tickets | Average Resolution Hours |
|---|---:|---:|
"""

    for priority, count in sorted(priority_counts.items()):
        summary += f"| {priority} | {count} | {avg_resolution_by_priority[priority]:.2f} |\n"

    summary += "\n## Top Ticket Categories\n\n| Category | Tickets |\n|---|---:|\n"
    for category, count in category_counts.most_common(7):
        summary += f"| {category} | {count} |\n"

    summary += "\n## Top Root Causes\n\n| Root Cause | Tickets |\n|---|---:|\n"
    for root_cause, count in root_cause_counts.most_common(7):
        summary += f"| {root_cause} | {count} |\n"

    summary += """
## Recommendations

1. Build or improve knowledge articles for the most common ticket categories.
2. Review repeat root causes and create preventive fixes instead of only resolving tickets.
3. Watch SLA misses by priority to identify staffing, training, or escalation gaps.
4. Use this dashboard monthly to measure whether improvements are reducing repeat work.

## Interview Talking Point

This project shows how I can take raw operational data, organize it, analyze patterns, and turn it into business recommendations. 
The goal is not just to close tickets faster; it is to identify repeatable causes, reduce preventable work, and improve the customer experience.
"""

    (REPORTS_DIR / "summary.md").write_text(summary, encoding="utf-8")
    print(f"Report written to {REPORTS_DIR / 'summary.md'}")


def main() -> None:
    rows = read_tickets()
    write_summary(rows)


if __name__ == "__main__":
    main()
