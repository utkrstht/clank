from dotenv import load_dotenv
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
