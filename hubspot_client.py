import requests
from config import Settings

BASE = "https://api.hubapi.com"

def search_contact_by_email(email: str) -> dict | None:
    url = f"{BASE}/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {Settings.HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    body = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }],
        "properties": [
            "email",
            "firstname",
            "lastname",
        ],
        "limit": 2
    }
    r = requests.post(url, json=body, headers=headers, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    if len(results) == 0:
        return None
    if len(results) > 1:
        raise RuntimeError(f"Multiple HubSpot contacts found for email: {email}")
    return results[0]