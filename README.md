# IT Operations Ticket Intelligence Lab

A practical GitHub portfolio project showing how IT support, customer success, and operations data can be turned into measurable business insight.

## Why this project exists

Many IT teams are reactive. They wait for tickets, fix the issue, and move on. This project shows a better approach: use ticket data to find patterns, identify root causes, reduce repeat issues, and improve service delivery.

## Project workflow

1. Generate or load ticket data.
2. Store the data in CSV and SQLite.
3. Run analysis using Python and SQL.
4. Identify SLA misses, escalations, repeat issues, and top root causes.
5. Convert the findings into an executive-style report.

## Repository structure

```text
github_it_operations_lab/
├── data/
│   ├── sample_tickets.csv
│   └── tickets.db
├── docs/
│   ├── architecture.md
│   ├── interview_talk_track.md
│   └── project_roadmap.md
├── reports/
│   └── summary.md
├── sql/
│   └── ticket_analysis.sql
├── src/
│   ├── analyze_tickets.py
│   └── generate_sample_data.py
├── .github/workflows/
│   └── python-check.yml
├── .gitignore
├── requirements.txt
└── README.md
```

## How to run it

```bash
pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_tickets.py
```

## Sample business questions answered

- Which ticket categories create the most work?
- Which root causes appear most often?
- Which priorities miss SLA the most?
- Which customer segments escalate most often?
- What issues should be fixed first to reduce repeat tickets?
