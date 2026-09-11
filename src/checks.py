import re
import requests

# This line (Line 6) of code was generated via generative AI (being Google AI Overview), search/prompt was "Regex for raw README validation case-insensitive"
RAW_README_REGEX = r"^https?:\/\/(?:raw\.githubusercontent\.com\/[^\/]+\/[^\/]+\/[^\/]+|gitlab\.com\/api\/v4\/projects\/[^\/]+\/repository\/files\/README(?:\.[a-zA-Z0-9]+)?\/raw|bitbucket\.org\/[^\/]+\/[^\/]+\/raw\/[^\/]+)\/README(?:\.[a-zA-Z0-9]+)?$"

# rejection reasons dictionary 
rejection_reasons = {"raw_readme":"Your raw README link is not raw, please update it.", "ai_readme":"Your README appears to be AI-generated, please re-write it by hand.", "ai_code":"Your codebase appears to be heavily AI-generated with little human effort, please re-write most of your code by hand.", "404_repo": "Your repository is either non-existent or privated, please fix this issue.", "404_demo": "Your demo link is either non-existent or private, please fix this issue", "banned_hosting_provider": "Your demo is hosted on an On-Activity Wake-Up hosting service, these take a very long time to load, please switch to an Always-On hosting service such as Hack Club Nest, Railway and Vercel.", "short_readme": "Your README lacks detail, please add more details such as, how you made it, why you made it, screenshots, features and anything else you wish to add."}
reject_reasons = []

# checks
def raw_readme_check(readme):
    if re.match(RAW_README_REGEX, readme, re.IGNORECASE):
        reject_reasons.append(rejection_reasons["raw_readme"]) 

def private_repo_demo_check(repo, demo):
    repo_response = requests.get(repo)
    demo_response = requests.get(demo)

    if repo_response.status_code == 200 and demo_response.status_code == 200:
        return
    elif repo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_repo"])
    elif demo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_demo"])
    elif repo_response.status_code == 403 and repo_response.headers.get("X-RateLimit-Remaining") == 0 or demo_response.status_code == 403 and demo_response.headers.get("X-RateLimit-Remaining") == 0:
        pass # TODO: handle ratelimit case

def run_all_checks(readme, repo, demo):
    raw_readme_check(readme)
    private_repo_demo_check(repo, demo)

    return reject_reasons
# TODO: add all checks