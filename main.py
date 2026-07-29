import os
from dotenv import load_dotenv
from auth import create_session
from api import get_advisory_feed
from storage import store_advisories

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
API_PREFIX = os.getenv("API_PREFIX")
PUBLIC_API_PREFIX = os.getenv("PUBLIC_API_PREFIX")

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

with create_session(client_id=client_id, client_secret=client_secret) as session:
    print("querying advisory feed")
    params = {
        "modified_since": "2026-06-30T20:27:36.860000+00:00",
        "limit": 50,
        #"include_purls": True
    }

    advisories, page_timings, total_elapsed, watermark = get_advisory_feed(session, params)
    store_result = store_advisories(advisories)

    print(
        f"stored {store_result['total']} advisories"
        f"({store_result['inserted']} inserted, {store_result['updated']} updated)"
    )
