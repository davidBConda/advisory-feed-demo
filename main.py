import os
from dotenv import load_dotenv
from auth import create_session
from api import get_advisory_feed
from db import get_session
from storage import record_feed_run, upsert_advisories

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
API_PREFIX = os.getenv("API_PREFIX")
PUBLIC_API_PREFIX = os.getenv("PUBLIC_API_PREFIX")

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

with create_session(client_id=client_id, client_secret=client_secret) as http_session:
    print("querying advisory feed")
    params = {
        "modified_since": "2026-07-15T00:00:00.000000+00:00",
        "limit": 50,
        #"include_purls": True
    }

    advisories, page_timings, total_elapsed, watermark = get_advisory_feed(http_session, params)

with get_session() as session:
    result = upsert_advisories(session, advisories)
    run = record_feed_run(
        session,
        query_params=params,
        watermark=watermark,
        fetch_duration_sec=total_elapsed,
        advisories_fetched=len(advisories),
        inserted=result["inserted"],
        updated=result["updated"],
        total=result["total"],
    )
    print(
        f"stored {result['total']} advisories "
        f"({result['inserted']} inserted, {result['updated']} updated); "
        f"run #{run.id} in {run.fetch_duration_sec:.3f}s"
    )
