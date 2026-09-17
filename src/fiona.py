from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
import os

load_dotenv()

SESSION = os.environ.get("SHIPWRIGHTS_SESSION")

def get_pending_projects():
    url = "https://ds.shipwrights.dev/api/v1/workplaces/stardance/certifications"
    cookies = {"session": SESSION}
    params = {"status": "PENDING", "page": 1}

    all_certs = []
    while True:
        response = requests.get(url, cookies=cookies, params=params)
        response.raise_for_status()

        data = response.json()
        all_certs.extend(data["certs"])

        if params["page"] >= data["pages"]:
            break

        params["page"] += 1
    return all_certs

def get_cert(link):
    id = urlparse(link).path.rstrip("/").split("/")[-1]
    url = f"https://ds.shipwrights.dev/api/v1/workplaces/stardance/certifications/{id}"
    cookies = {"session": SESSION}

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    return response.json()

def claim_cert(id):
    url = f"https://ds.shipwrights.dev/api/v1/workplaces/stardance/certifications/{id}/claim"
    cookies = {"session": SESSION}

    response = requests.post(url, cookies=cookies, json={"unclaim": False})
    response.raise_for_status()

    return response.json()

def submit_review(id, verdict, feedback):
    url = f"https://ds.shipwrights.dev/api/v1/workplaces/stardance/certifications/{id}/review"
    cookies = {"session": SESSION}

    response = requests.post(url, cookies=cookies, json={
        "verdict": verdict,
        "comment": feedback
    })
    response.raise_for_status()

    return response.json()
