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

if __name__ == "__main__":
    print(get_cert("https://ds.shipwrights.dev/stardance/certifications/be51e324-bac3-42b8-b638-c7b414812fbb"))