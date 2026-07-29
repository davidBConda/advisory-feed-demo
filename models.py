from typing import Any, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Advisory(SQLModel, table=True):
    __tablename__ = "advisories"

    advisory_id: str = Field(primary_key=True)
    data: dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    created_at: str
    updated_at: str


class FeedRun(SQLModel, table=True):
    __tablename__ = "feed_runs"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: str
    query_params: dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    watermark: str = ""
    fetch_duration_sec: float
    advisories_fetched: int
    inserted: int
    updated: int
    total: int
