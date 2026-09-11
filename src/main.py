import argparse
import requests
import re

# holy shit
RAW_README_REGEX = r"^https?:\/\/(?:raw\.githubusercontent\.com\/[^\/]+\/[^\/]+\/[^\/]+|gitlab\.com\/api\/v4\/projects\/[^\/]+\/repository\/files\/README(?:\.[a-zA-Z0-9]+)?\/raw|bitbucket\.org\/[^\/]+\/[^\/]+\/raw\/[^\/]+)\/README(?:\.[a-zA-Z0-9]+)?$"

# rejection reasons dictionary 
rejection_reasons = {"raw_readme":"Your raw README link is not raw, please update it.", "ai_readme":"Your README appears to be AI-generated, please re-write it by hand.", "ai_code":"Your codebase appears to be heavily AI-generated with little human effort, please re-write most of your code by hand.", "404_repo": "Your repository is either non-existent or privated, please fix this issue.", "404_demo": "Your demo link is either non-existent or private, please fix this issue", "banned_hosting_provider": "Your demo is hosted on an On-Activity Wake-Up hosting service, these take a very long time to load, please switch to an Always-On hosting service such as Hack Club Nest, Railway and Vercel.", "short_readme": "Your README lacks detail, please add more details such as, how you made it, why you made it, screenshots, features and anything else you wish to add."}
reject_reasons = []

def create_rejection_message(rejection_reasons):
    template = f"""Hello, your project has the following issues, please fix them for approval:
    {"\n".join(f"- {item}" for item in rejection_reasons)}
    If you have any questions, DM @kaboom or create a ticket in #ask-the-shipwrights. """\

    return template
        
parser = argparse.ArgumentParser(description="clank it up 🚀✨ (this is a joke)")

# setup basic review inputs
parser.add_argument("--repo", type=str, help="GitHub Repository Link")
parser.add_argument("--readme", type=str, help="Raw README Link")
parser.add_argument("--stardance", type=str, help="Stardance Project Link")
parser.add_argument("--demo", type=str, help="Demo Link")

args = parser.parse_args()

# checks
def raw_readme_check():
    if re.match(RAW_README_REGEX, args.readme, re.IGNORECASE):
        reject_reasons.append(rejection_reasons["raw_readme"]) 

# 404 repo check
def private_repo_demo_check():
    repo_response = requests.get(args.repo)
    demo_response = requests.get(args.demo)

    if repo_response.status_code == 200 and demo_response.status_code == 200:
        return
    elif repo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_repo"])
    elif demo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_demo"])
    elif repo_response.status_code == 403 and repo_response.headers.get("X-RateLimit-Remaining") == 0 or demo_response.status_code == 403 and demo_response.headers.get("X-RateLimit-Remaining") == 0:
        pass # TODO: handle ratelimit case
    
# TODO: add all checks
# TODO: refactor functions