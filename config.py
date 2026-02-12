# import os
# from dotenv import load_dotenv

# load_dotenv()

# def must_get(name: str) -> str:
#     v = os.getenv(name)
#     if not v:
#         raise RuntimeError(f"Missing required env var: {name}")
#     return v

# class Settings:
#     NOTION_TOKEN = must_get("NOTION_TOKEN")
#     NOTION_PROFILES_DB_ID = must_get("NOTION_PROFILES_DB_ID")
#     NOTION_TEAMS_DB_ID = must_get("NOTION_TEAMS_DB_ID")
#     NOTION_PARENT_ONBOARDING_PAGE_ID = must_get("NOTION_PARENT_ONBOARDING_PAGE_ID")
#     NOTION_PARENT_MASTERCLASSES_PAGE_ID = must_get("NOTION_PARENT_MASTERCLASSES_PAGE_ID")

#     HUBSPOT_ACCESS_TOKEN = must_get("HUBSPOT_ACCESS_TOKEN")

#     EMAIL_MODE = os.getenv("EMAIL_MODE", "link")