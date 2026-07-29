import os
import requests
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
API_PREFIX = os.getenv("API_PREFIX")

def _get_auth_token(grant_type: str = "password", **credentials) -> str:
    if "username" in credentials:
        grant_type = "password"
    elif "client_id" in credentials:
        grant_type = "client_credentials"
    else:
        raise ValueError("Invalid credentials")

    response = requests.post(
        f"{HOSTNAME}{API_PREFIX}/iam/token",
        data=dict(**credentials, grant_type=grant_type),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_session(**kwargs):
    token = _get_auth_token(**kwargs)
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session
