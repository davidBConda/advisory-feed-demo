from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Session, select

from models import Advisory, FeedRun


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def upsert_advisories(session: Session, advisories: list[dict[str, Any]]) -> dict[str, int]:
    if not advisories:
        return {"inserted": 0, "updated": 0, "total": 0}

    now = _utc_now()
    rows = []
    for advisory in advisories:
        advisory_id = advisory.get("advisory_id")
        if not advisory_id:
            raise ValueError("advisory missing advisory_id")
        rows.append(
            {
                "advisory_id": advisory_id,
                "data": advisory,
                "created_at": now,
                "updated_at": now,
            }
        )

    before_count = session.exec(select(func.count()).select_from(Advisory)).one()

    stmt = insert(Advisory).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["advisory_id"],
        set_={
            "data": stmt.excluded.data,
            "updated_at": stmt.excluded.updated_at,
        },
    )
    session.execute(stmt)
    session.commit()

    after_count = session.exec(select(func.count()).select_from(Advisory)).one()
    inserted = after_count - before_count
    updated = len(rows) - inserted
    return {"inserted": inserted, "updated": updated, "total": len(rows)}


def record_feed_run(
    session: Session,
    *,
    query_params: dict[str, Any],
    watermark: str,
    fetch_duration_sec: float,
    advisories_fetched: int,
    inserted: int,
    updated: int,
    total: int,
) -> FeedRun:
    if not watermark:
        previous = latest_feed_run(session)
        if previous and previous.watermark:
            watermark = previous.watermark

    run = FeedRun(
        created_at=_utc_now(),
        query_params=query_params,
        watermark=watermark,
        fetch_duration_sec=fetch_duration_sec,
        advisories_fetched=advisories_fetched,
        inserted=inserted,
        updated=updated,
        total=total,
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def latest_feed_run(session: Session) -> FeedRun | None:
    return session.exec(select(FeedRun).order_by(FeedRun.id.desc())).first()


def latest_watermark(session: Session) -> str | None:
    return session.exec(
        select(FeedRun.watermark)
        .where(FeedRun.watermark != "")
        .order_by(FeedRun.id.desc())
    ).first()
