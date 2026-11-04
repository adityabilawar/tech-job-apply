"""Private application state and append-ordered event export."""
import argparse
import csv
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from contextlib import closing

TRANSITIONS = {
    "claimed": {"prepared", "skipped"},
    "prepared": {"submitting", "skipped"},
    "submitting": {"submitted", "unknown"},
    "unknown": {"submitted", "skipped"},
}
ACTIVE = ("claimed", "prepared", "submitting", "unknown")


def record(db, job, stage, token, evidence=None):
    db.execute(
        """INSERT INTO jobs VALUES (?, ?, ?, ?)
           ON CONFLICT(job_id) DO UPDATE SET
           stage=excluded.stage, token=excluded.token, evidence=excluded.evidence""",
        (job, stage, token, evidence),
    )
    db.execute(
        "INSERT INTO events(job_id, stage, evidence) VALUES (?, ?, ?)",
        (job, stage, evidence),
    )


def run(db, args):
    if args.command in {"status", "export"}:
        query = "SELECT job_id, stage, evidence FROM jobs ORDER BY job_id"
        if args.command == "export" and args.format == "jsonl":
            query = "SELECT id, at, job_id, stage, evidence FROM events ORDER BY id"
        rows = db.execute(query)
        if args.command == "export" and args.format == "csv":
            writer = csv.writer(sys.stdout)
            writer.writerow(column[0] for column in rows.description)
            writer.writerows(
                [("'" + value) if value and value.lstrip().startswith(
                    ("=", "+", "-", "@")) else value for value in row]
                for row in rows
            )
        else:
            for row in rows:
                print(json.dumps(dict(row)))
        return

    db.execute("BEGIN IMMEDIATE")
    job = args.job_id
    row = db.execute("SELECT * FROM jobs WHERE job_id=?", (job,)).fetchone()
    if args.command == "claim":
        active = db.execute(
            "SELECT job_id FROM jobs WHERE stage IN (?, ?, ?, ?)", ACTIVE
        ).fetchone()
        if active or row:
            raise ValueError("An application is active or this job is already tracked.")
        stage = "claimed"
        token = secrets.token_urlsafe(24)
    elif args.command == "recover":
        if not row or row["stage"] not in ACTIVE:
            raise ValueError("Recovery requires an active application.")
        stage = "unknown" if row["stage"] == "submitting" else row["stage"]
        token = secrets.token_urlsafe(24)
    else:
        if not row or not secrets.compare_digest(row["token"], args.token):
            raise ValueError("Invalid claim credentials.")
        stage, token = args.stage, row["token"]
        if stage not in TRANSITIONS.get(row["stage"], set()):
            raise ValueError("Invalid stage transition.")
        if (stage == "submitted" or (row["stage"] == "unknown" and stage == "skipped")):
            if not (args.evidence or "").strip():
                raise ValueError("Confirmation evidence or reconciliation reason required.")
    record(db, job, stage, token, getattr(args, "evidence", None))
    db.commit()
    result = {"job_id": job, "stage": stage}
    if args.command in {"claim", "recover"}:
        result["token"] = token
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    commands.add_parser("export").add_argument("format", choices=("csv", "jsonl"))
    commands.add_parser("claim").add_argument("job_id")
    recover = commands.add_parser("recover")
    recover.add_argument("job_id")
    recover.add_argument("--previous-applier-stopped", required=True, action="store_true")
    move = commands.add_parser("move")
    move.add_argument("job_id")
    move.add_argument("token")
    move.add_argument("stage")
    move.add_argument("--evidence")
    args = parser.parse_args()

    os.umask(0o077)
    root = Path(os.environ.get("TECH_JOB_APPLY_HOME", Path.home() / ".tech-job-apply"))
    try:
        if not root.is_absolute():
            raise ValueError("TECH_JOB_APPLY_HOME must be absolute.")
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        path = root / "applications.sqlite3"
        if root.stat().st_mode & 0o077 or (path.exists() and path.stat().st_mode & 0o077):
            raise ValueError("Storage permissions must exclude group and other users.")
        with closing(sqlite3.connect(path)) as db:
            db.row_factory = sqlite3.Row
            db.executescript("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY, stage TEXT NOT NULL,
                    token TEXT NOT NULL, evidence TEXT
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                    job_id TEXT NOT NULL, stage TEXT NOT NULL, evidence TEXT
                );
            """)
            run(db, args)
    except (ValueError, OSError, sqlite3.Error) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
