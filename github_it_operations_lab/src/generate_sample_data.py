"""
Generate synthetic IT ticket data for the IT Operations Ticket Intelligence Lab.

This script creates:
- data/sample_tickets.csv
- data/tickets.db

The data is synthetic and safe to share publicly.
"""

from pathlib import Path
import csv
import random
import sqlite3
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)

CATEGORIES = ["Access", "Network", "Device", "Software", "Security", "Billing", "Mobile Device Management"]
PRIORITIES = ["P1", "P2", "P3", "P4"]
TEAMS = ["Help Desk", "Network Ops", "Security", "Endpoint Support", "Customer Success"]
SEGMENTS = ["Enterprise", "Healthcare", "Government", "Small Business"]
ROOT_CAUSES = [
    "Password reset process gap",
    "Device enrollment issue",
    "Carrier provisioning delay",
    "Expired certificate",
    "VPN configuration drift",
    "Outdated knowledge article",
    "User training gap",
    "Hardware failure",
    "Firewall rule mismatch",
    "License assignment issue",
]
STATUSES = ["Resolved", "Resolved", "Resolved", "Closed", "Open"]
SLA_BY_PRIORITY = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}


def build_rows(total_rows: int = 300) -> list[dict]:
    rows = []
    start_date = datetime(2026, 1, 1)

    for i in range(1, total_rows + 1):
        priority = random.choices(PRIORITIES, weights=[8, 18, 44, 30], k=1)[0]
        category = random.choices(CATEGORIES, weights=[24, 13, 14, 15, 8, 10, 16], k=1)[0]
        created = start_date + timedelta(
            days=random.randint(0, 149),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        sla_hours = SLA_BY_PRIORITY[priority]

        if priority == "P1":
            resolution_hours = random.uniform(1, 10)
        elif priority == "P2":
            resolution_hours = random.uniform(2, 20)
        elif priority == "P3":
            resolution_hours = random.uniform(4, 60)
        else:
            resolution_hours = random.uniform(6, 120)

        status = random.choice(STATUSES)
        resolved = created + timedelta(hours=resolution_hours) if status in ["Resolved", "Closed"] else ""
        first_response_hours = max(0.1, resolution_hours * random.uniform(0.05, 0.35))
        sla_met = "Yes" if resolution_hours <= sla_hours else "No"
        escalated = "Yes" if priority in ["P1", "P2"] and random.random() < 0.38 else (
            "Yes" if random.random() < 0.08 else "No"
        )

        rows.append({
            "ticket_id": f"INC-{i:05d}",
            "created_at": created.isoformat(timespec="minutes"),
            "resolved_at": resolved.isoformat(timespec="minutes") if resolved else "",
            "status": status,
            "priority": priority,
            "category": category,
            "assigned_team": random.choice(TEAMS),
            "customer_segment": random.choice(SEGMENTS),
            "root_cause": random.choice(ROOT_CAUSES),
            "sla_hours": sla_hours,
            "resolution_hours": round(resolution_hours, 2),
            "first_response_hours": round(first_response_hours, 2),
            "sla_met": sla_met,
            "escalated": escalated,
        })

    return rows


def write_csv(rows: list[dict]) -> None:
    csv_path = DATA_DIR / "sample_tickets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_sqlite(rows: list[dict]) -> None:
    db_path = DATA_DIR / "tickets.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tickets")
    cursor.execute("""
    CREATE TABLE tickets (
        ticket_id TEXT PRIMARY KEY,
        created_at TEXT,
        resolved_at TEXT,
        status TEXT,
        priority TEXT,
        category TEXT,
        assigned_team TEXT,
        customer_segment TEXT,
        root_cause TEXT,
        sla_hours INTEGER,
        resolution_hours REAL,
        first_response_hours REAL,
        sla_met TEXT,
        escalated TEXT
    )
    """)

    for row in rows:
        cursor.execute("""
        INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(row.values()))

    conn.commit()
    conn.close()


def main() -> None:
    rows = build_rows()
    write_csv(rows)
    write_sqlite(rows)
    print(f"Generated {len(rows)} synthetic tickets in {DATA_DIR}")


if __name__ == "__main__":
    main()
