import os
from dotenv import load_dotenv
import time

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
PUBLIC_API_PREFIX = os.getenv("PUBLIC_API_PREFIX")
API_URL = f"{HOSTNAME}{PUBLIC_API_PREFIX}/advisories"

def get_advisory(session, advisory_id, params=None):
    resp = session.get(f"{API_URL}/{advisory_id}", params=params)
    resp.raise_for_status()
    return resp.json()

def get_advisory_feed(session, params=None):
    advisories = []
    page_timings = []
    url = f"{API_URL}/feed"
    request_params = params
    page_num = 0
    total_start = time.perf_counter()
    watermark = ""

    while True:
        start = time.perf_counter()
        response = session.get(url, params=request_params)
        response.raise_for_status()
        elapsed = time.perf_counter() - start
        data = response.json()
        if page_num == 0:
            watermark = data.get("watermark", "")
        page_advisories = data.get("advisories", [])
        advisories.extend(page_advisories)
        page_timings.append({
            "page": page_num,
            "duration_sec": elapsed,
            "advisories_count": len(page_advisories),
        })
        print(f"page {page_num}: {elapsed:.3f}s ({len(page_advisories)} advisories)")

        if not data.get("has_more"):
            break

        url = f"{HOSTNAME}{data['next_url']}"
        page_num += 1

    return advisories, page_timings, time.perf_counter() - total_start, watermark