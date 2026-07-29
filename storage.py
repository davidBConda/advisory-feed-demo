import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent / "advisories.db"

_ADVISORIES_TABLE = """
CREATE TABLE IF NOT EXISTS advisories (
    advisory_id TEXT NOT NULL PRIMARY KEY,
    data JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
"""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _table_columns(conn: sqlite3.Connection) -> set[str]:
    return {row[1] for row in conn.execute("PRAGMA table_info(advisories)")}


def _migrate_schema(conn: sqlite3.Connection) -> None:
    columns = _table_columns(conn)
    if not columns:
        return

    if "advisory_id" not in columns:
        conn.execute("ALTER TABLE advisories RENAME TO advisories_old")
        conn.execute(_ADVISORIES_TABLE)

        now = _utc_now()
        for (data,) in conn.execute("SELECT data FROM advisories_old"):
            advisory = json.loads(data)
            advisory_id = advisory.get("advisory_id")
            if advisory_id:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO advisories (advisory_id, data, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (advisory_id, data, now, now),
                )

        conn.execute("DROP TABLE advisories_old")
        columns = _table_columns(conn)

    now = _utc_now()
    if "created_at" not in columns:
        conn.execute(
            f"ALTER TABLE advisories ADD COLUMN created_at TEXT NOT NULL DEFAULT '{now}'"
        )
    if "updated_at" not in columns:
        conn.execute(
            f"ALTER TABLE advisories ADD COLUMN updated_at TEXT NOT NULL DEFAULT '{now}'"
        )

    conn.commit()


def init_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(_ADVISORIES_TABLE)
    _migrate_schema(conn)
    conn.commit()
    return conn


def store_advisories(
    advisories: list[dict],
    conn: sqlite3.Connection | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> dict[str, int]:
    if not advisories:
        return {"inserted": 0, "updated": 0, "total": 0}

    close_conn = conn is None
    if conn is None:
        conn = init_db(db_path)

    try:
        now = _utc_now()
        rows = []
        for advisory in advisories:
            advisory_id = advisory.get("advisory_id")
            if not advisory_id:
                raise ValueError("advisory missing advisory_id")
            rows.append((advisory_id, json.dumps(advisory), now, now))

        before_count = conn.execute("SELECT COUNT(*) FROM advisories").fetchone()[0]
        conn.executemany(
            """
            INSERT INTO advisories (advisory_id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(advisory_id) DO UPDATE SET
                data = excluded.data,
                updated_at = excluded.updated_at
            """,
            rows,
        )
        conn.commit()

        after_count = conn.execute("SELECT COUNT(*) FROM advisories").fetchone()[0]
        inserted = after_count - before_count
        updated = len(rows) - inserted
        return {"inserted": inserted, "updated": updated, "total": len(rows)}
    finally:
        if close_conn:
            conn.close()
