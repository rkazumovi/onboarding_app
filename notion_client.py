import requests
from config import Settings

BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def _headers():
    return {
        "Authorization": f"Bearer {Settings.NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

def query_profile_by_email(email: str) -> list[dict]:
    url = f"{BASE}/databases/{Settings.NOTION_PROFILES_DB_ID}/query"
    body = {
        "filter": {
            "property": "Email",
            "email": {"equals": email}
        }
    }
    r = requests.post(url, headers=_headers(), json=body, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])

def create_profile(properties: dict) -> dict:
    url = f"{BASE}/pages"
    body = {
        "parent": {"database_id": Settings.NOTION_PROFILES_DB_ID},
        "properties": properties
    }
    r = requests.post(url, headers=_headers(), json=body, timeout=30)
    r.raise_for_status()
    return r.json()