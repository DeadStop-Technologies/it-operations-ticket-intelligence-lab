# Architecture

```mermaid
flowchart LR
    A[Ticket Data CSV] --> B[Python Analysis Script]
    A --> C[SQLite Database]
    C --> D[SQL Queries]
    B --> E[Executive Summary Report]
    D --> F[Operational Insights]
    E --> G[Interview Portfolio]
    F --> G
```

## What this shows

This project connects technical work to business outcomes.

- CSV shows basic data handling.
- SQLite shows database fundamentals.
- SQL queries show structured analysis.
- Python script shows automation.
- Markdown report shows business communication.
- GitHub Actions shows basic CI/CD awareness.
