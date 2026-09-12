from emoji import emoji_count
from utils import calculate_ratelimit, is_banned_domain
from time import sleep
import re
import requests


# This line of code was generated via generative AI (being Google AI Overview), search/prompt was "Regex for raw README validation case-insensitive"
RAW_README_REGEX = r"^https?:\/\/(?:raw\.githubusercontent\.com\/[^\/]+\/[^\/]+\/[^\/]+|gitlab\.com\/api\/v4\/projects\/[^\/]+\/repository\/files\/README(?:\.[a-zA-Z0-9]+)?\/raw|bitbucket\.org\/[^\/]+\/[^\/]+\/raw\/[^\/]+)\/README(?:\.[a-zA-Z0-9]+)?$"

# rejection reasons dictionary 
rejection_reasons = {"raw_readme":"Your raw README link is not raw, please update it.", "no_readme":"Your project repository does not have a README, please create one with information such as, how you made it, why you made it, screenshots, features and anything else you wish to add.", "ai_readme":"Your README appears to be AI-generated, please re-write it by hand.", "ai_code":"Your codebase appears to be heavily AI-generated with little human effort, please re-write most of your code by hand.", "404_repo": "Your repository is either non-existent or privated, please fix this issue.", "404_demo": "Your demo link is either non-existent or private, please fix this issue", "banned_hosting_provider": "Your demo is hosted on an On-Activity Wake-Up hosting service, these take a very long time to load or it's hosted on a local tunneled server which can go down anytime or it's hosted on huggingface, which we do not allow, please switch to an Always-On hosting service such as Hack Club Nest, Railway and Vercel.", "short_readme": "Your README lacks detail, please add more details such as, how you made it, why you made it, screenshots, features and anything else you wish to add.", "repo_demo_same": "Your repository and demo links are the same, Your demo link cannot be the same as your repository link, it needs to be of a website if you made a webapp, or a compiled binary on Github Releases, or a library hosted on NPM or PyPi or some other platform depending on your project or a mod hosting website like ModRinth or CurseForge if you have a minecraft mod."}
reject_reasons = []

# checks
def raw_readme_check(readme):
    if re.match(RAW_README_REGEX, readme, re.IGNORECASE):
        reject_reasons.append(rejection_reasons["raw_readme"]) 
        return

    response = requests.get(readme)

    if response.status_code == 200:
        return
    elif response.status_code == 404:
        reject_reasons.append(rejection_reasons["no_readme"])
        return "No Readme"
    elif response.status_code == 403 and int(response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(response))
        raw_readme_check(readme)

def private_repo_check(repo):
    repo_response = requests.get(repo)

    if repo_response.status_code == 200:
        return
    elif repo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_repo"])
        return "Private Repo"
    elif repo_response.status_code == 403 and int(repo_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(repo_response))
        # recursion!!! 🚀😍
        private_repo_check(repo)


def private_demo_check(demo):
    demo_response = requests.get(demo)

    if demo_response.status_code == 200:
        return
    elif demo_response.status_code == 404:
        reject_reasons.append(rejection_reasons["404_demo"])
        return "Private Demo"
    elif demo_response.status_code == 403 and int(demo_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(demo_response))
        # recursion!!! 🚀😍
        private_demo_check(demo)

def ai_readme_check(readme):
    response = requests.get(readme)
    if response.status_code == 200:
        readme_text = response.text
        if readme_text.count("—") >= 1 or emoji_count(readme_text) >= 3:
            reject_reasons.append(rejection_reasons["ai_readme"])
            # TODO: make more accurate 

def hosting_provider_check(demo, repo):
    if is_banned_domain(demo):
        reject_reasons.append(rejection_reasons["banned_hosting_provider"])
    elif repo in demo or demo in repo:
        reject_reasons.append(rejection_reasons["repo_demo_same"])
    else:
        return

def short_empty_readme(readme):
    response = requests.get(readme)
    if response.status_code == 200:
        if len(response.text) <= 500:
            reject_reasons.append(rejection_reasons["short_readme"])

def run_all_checks(readme, repo, demo):
    if raw_readme_check(readme) != "No Readme":
        ai_readme_check(readme)
        short_empty_readme(readme)

    if private_repo_check(repo) != "Private Repo" and private_demo_check(demo) != "Private Demo":
        hosting_provider_check(demo, repo)

    return reject_reasons

# TODO: optimize checks as they currently send a lot of requests to GitHub for the same thing, and GitHub only allows 60 rph for no auth requests.
# TODO: add all checks
# TODO: specifically implement some minor checks for project banner