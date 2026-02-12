import requests
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
import hashlib
import logging
# from config import Settings
# settings = Settings()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("onboarding")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
def submit_form(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    teams: list[str] = Form(...),
):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "teams": teams,
    }

    log.info(f"Received payload: {payload}")

    response = requests.post(
    "https://searchcompareshare.com/webhook-test/4fcdb8bc-170c-422b-af28-6b0a0339e804",
    json=payload,
    timeout=10
)

    log.info(f"n8n response: {response.status_code}")

    return {"status": "sent to n8n"}

# @app.post("/submit")
# def submit_form(
#     first_name: str = Form(...),
#     last_name: str = Form(...),
#     email: str = Form(...),
#     teams: list[str] = Form(...),
# ):
#     payload = {
#         "first_name": first_name,
#         "last_name": last_name,
#         "email": email,
#         "teams": teams,
#     }

#     response = requests.post(
#         "https://searchcompareshare.com/webhook-test/onboarding-form",
#         json=payload,
#         timeout=10
#     )

#     return {"status": "sent to n8n"}

@app.post("/onboard")
def onboard(payload: dict):
    try:
        # Step 1: Check HubSpot
        hubspot_data = search_contact_by_email(payload['email'])
        if not hubspot_data:
            raise HTTPException(status_code=404, detail="HubSpot contact not found")

        # Step 2: Check for existing profile in Notion
        existing_profile = query_profile_by_email(payload['email'])
        if existing_profile:
            return {"status": "Profile already exists", "profile_id": existing_profile[0]["id"]}

        # Step 3: Create Profile in Notion
        profile = create_profile(payload)  # Assuming this function creates a Notion page for the profile
        if not profile:
            raise HTTPException(status_code=500, detail="Error creating Notion profile")

        # Step 4: Generate agreement docx
        agreement_file = generate_agreement(payload)

        # Step 5: Upload the agreement docx to Notion (and attach to profile)
        upload_agreement_to_notion(profile['id'], agreement_file)

        # Step 6: Create Onboarding and MasterClass pages in Notion
        create_onboarding_page(profile['id'])
        create_masterclass_pages(payload['teams'])

        # Step 7: Send email (with agreement link or attachment)
        send_email(payload['email'], agreement_file)

        return {"status": "Onboarding complete", "profile_url": profile['url']}
    except Exception as e:
        log.error(f"Error in onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in onboarding process: {str(e)}")

# venv\Scripts\activate
# uvicorn main:app --reload
