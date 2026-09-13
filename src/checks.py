from emoji import emoji_count
from utils import calculate_ratelimit, is_banned_domain, get_repository_default_branch, get_repository_tree, get_file, count_comments, count_docstrings
from time import sleep
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv
import c2pa
import re
import json
import requests
import os

# This line of code was generated via generative AI (being Google AI Overview), search/prompt was "Regex for raw README validation case-insensitive"
RAW_README_REGEX = r"^https?:\/\/(?:raw\.githubusercontent\.com\/[^\/]+\/[^\/]+\/[^\/]+|gitlab\.com\/api\/v4\/projects\/[^\/]+\/repository\/files\/README(?:\.[a-zA-Z0-9]+)?\/raw|bitbucket\.org\/[^\/]+\/[^\/]+\/raw\/[^\/]+)\/README(?:\.[a-zA-Z0-9]+)?$"

# This list was generated via generative AI (being Google AI Overview), search/prompt was "All source code extensions in a python list" and then modified by a human to remove unnecessary extensions
source_extensions = [
    ".html", ".htm", ".css", ".js", ".mjs", ".ts", ".tsx", ".php", ".jsx",
    ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hxx", ".cs", ".java", 
    ".class", ".go", ".rs", ".swift", ".kt", ".kts", ".py", ".pyw", 
    ".ipynb", ".r", ".sh", ".bat", ".cmd", ".ps1", ".rb", ".pl", ".pm",
    ".dart", ".scala", ".lua", ".hs", ".clj", ".ex", ".exs", ".erl", ".hrl",
    ".groovy", ".fs", ".ml", ".pas", ".asm", ".s", ".md"
]

# rejection reasons dictionary 
rejection_reasons = {"raw_readme":"Your raw README link is not raw, please update it.", 
                     "no_readme":"Your project repository does not have a README, please create one with information such as, how you made it, why you made it, screenshots, features and anything else you wish to add.", 
                     "ai_readme":"Your README appears to be AI-generated, please re-write it by hand.", 
                     "ai_code":"Your codebase appears to be heavily AI-generated with little human effort, please re-write most of your code by hand.", 
                     "404_repo": "Your repository is either non-existent or privated, please fix this issue.", 
                     "404_demo": "Your demo link is either non-existent or private, please fix this issue", 
                     "banned_hosting_provider": "Your demo is either hosted on an On-Activity Wake-Up hosting service, these take a very long time to load or it's hosted on a local tunneled server which can go down anytime or it's hosted on huggingface, which we do not allow or it's hosted on youtube, which we do not allow video demos., please switch to an Always-On hosting service such as Hack Club Nest, Railway and Vercel.", 
                     "short_readme": "Your README lacks detail, please add more details such as, how you made it, why you made it, screenshots, features and anything else you wish to add.", 
                     "repo_demo_same": "Your demo points to within your repository, however your demo link needs to be of a website if you made a webapp, or a compiled binary on Github Releases, or a library hosted on NPM or PyPi or some other platform depending on your project or a mod hosting website like ModRinth or CurseForge if you have a minecraft mod.",
                     "ai_banner": "Your Stardance project banner is AI-generated, please change it to show your project running and working. ",
                     "irrelevant_banner": "Your Stardance project banner is either a logo or not relevant to your project, the banner needs to be of your projects running and working, please update it."}
reject_reasons = []

load_dotenv()

# determine whether github requests are authenticated or not 
# unauthenticated -> 60 req/hr, authenticated -> 5000 req/hr
if os.environ.get("GITHUB_TOKEN"):
    GITHUB_AUTH = True
else:
    GITHUB_AUTH = False
    
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# determine whether code/text is ai
def ai_detector(content):
    # TODO: implement checks for docstrings, emojis, emdashes and non keyboard symbols
    comments = count_comments(content)
    emojis = len(emoji_count(content))
    # python only
    docstrings = count_docstrings(content)
    pass

# checks
def raw_readme_check(readme):
    if not re.match(RAW_README_REGEX, readme.url, re.IGNORECASE):
        reject_reasons.append(rejection_reasons["raw_readme"]) 
        return "Raw Readme Link is not raw"

    if readme.status_code == 404:
        reject_reasons.append(rejection_reasons["no_readme"])
        return "No Readme"

def private_repo_check(repo):
    if repo.status_code == 404:
        reject_reasons.append(rejection_reasons["404_repo"])
        return "Private Repo"

def private_demo_check(demo):
    if demo.status_code == 404:
        reject_reasons.append(rejection_reasons["404_demo"])
        return "Private Demo"

def ai_readme_check(readme):
    readme_text = readme.text
    if readme_text.count("—") >= 1 or emoji_count(readme_text) >= 3:
        reject_reasons.append(rejection_reasons["ai_readme"])
        return "AI Readme"
        # TODO: make more accurate 

def hosting_provider_check(demo, repo):
    if is_banned_domain(demo):
        reject_reasons.append(rejection_reasons["banned_hosting_provider"])
    elif repo in demo and not "releases" in demo:
        reject_reasons.append(rejection_reasons["repo_demo_same"])
        return "Demo points within Repo"
    else:
        return

def short_empty_readme(readme):
    if len(readme.text) <= 500:
        reject_reasons.append(rejection_reasons["short_readme"])
        return "Short Readme"

def c2pa_banner_check(stardance):
    soup = BeautifulSoup(stardance.text, "html.parser")
    banner = soup.find("img", class_="project-show__banner-image")
    # banner can sometimes be None
    if not banner:
        return
    banner_url = banner["src"]

    response = requests.get(banner_url)
    content_type = response.headers.get("Content-Type", "").split(";")[0]
    try:
        reader = c2pa.Reader(content_type, response.content)

        manifest = json.loads(reader.json())
        active = manifest["manifests"][manifest["active_manifest"]]

        for assertion in active.get("assertions", []):
            if assertion["label"] == "c2pa.actions":
                for action in assertion["data"]["actions"]:
                    if action.get("digitalSourceType") == "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia":
                        reject_reasons.append(rejection_reasons["ai_banner"])
                        return "AI Banner"
    except c2pa.C2paError as e:
        print("c2pa threw an exception (likely no c2pa data found):", e)
    except Exception as e:
        print("something happened lol:", e)

def project_banner_relevance_check(stardance):
    soup = BeautifulSoup(stardance.text, "html.parser")
    banner = soup.find("img", class_="project-show__banner-image")
    # banner can sometimes be None
    if not banner:
        return
    banner_url = banner["src"]
    response = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            reasoning_format="hidden",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are to determine whether the provided image is simply a logo, or if it shows a website, project, app, game or anything of the sort running, If you determine that the image is a logo/aesthetic banner, ONLY type 'logo/banner' with nothing else, if it isn't that, only type 'approve' with nothing else"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": banner_url}
                        }
                    ]
                }
            ]
        )

    raw = response.choices[0].message.content

    if "logo/banner" in raw:
        reject_reasons.append(rejection_reasons["irrelevant_banner"])
        return "Irrelevant Banner"
    if "approve" in raw:
        return

def ai_codebase_check(repo):
    # TODO: ai-ness will be determined via number of comments, emojis, em-dashes, non-keyboard symbols (eg. arrow symbol), also with CLAUDE.mds and agents and .agents/.claude folders
    # TODO: generate a confidence score (1-100) with the above metrics
    headers = {"Authorization": f"Bearer {os.environ.get("GITHUB_TOKEN")}"}
    
    # obtain repository files
    branch = get_repository_default_branch(repo, headers)
    tree = get_repository_tree(repo, branch, headers)

    # holy trippy wizard shit bro
    source_files = [ item for item in tree if item["type"] == "blob" and item["path"].endswith(source_extensions) ]

    # fetch file content
    for file in source_files:
        path = file["path"]
        sha = file["sha"]

        try:
            content = get_file(repo, sha, headers)
        except Exception as e:
            print(f"ohohoho whoops i fucked up (could not read {path} while fetching file): {e}")

def run_all_checks(readme, repo, demo, stardance):
    if GITHUB_AUTH and "github" in readme and "github" in repo:
        headers = {"Authorization": f"Bearer {os.environ.get("GITHUB_TOKEN")}"}
        readme_response = requests.get(readme, timeout=30, headers=headers)
        repo_response = requests.get(repo, timeout=30, headers=headers)
        demo_response = requests.get(demo, timeout=30)
        stardance_response = requests.get(stardance, timeout=30)
    else:  
        # unauthenticated
        readme_response = requests.get(readme, timeout=30)
        repo_response = requests.get(repo, timeout=30)
        demo_response = requests.get(demo, timeout=30)
        stardance_response = requests.get(stardance, timeout=30)

    # handle ratelimits
    if readme_response.status_code == 403 and int(readme_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(readme_response))
        readme_response = requests.get(readme)
    if repo_response.status_code == 403 and int(repo_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(repo_response))
        repo_response = requests.get(repo)
    if demo_response.status_code == 403 and int(demo_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(demo_response))
        demo_response = requests.get(demo)
    if stardance_response.status_code == 403 and int(stardance_response.headers.get("X-RateLimit-Remaining")) == 0:
        sleep(calculate_ratelimit(stardance_response))
        stardance_response = requests.get(stardance)


    if raw_readme_check(readme_response) != "No Readme":
        ai_readme_check(readme_response)
        short_empty_readme(readme_response)

    if private_repo_check(repo_response) != "Private Repo" and private_demo_check(demo_response) != "Private Demo":
        hosting_provider_check(demo, repo)

    c2pa_banner_check(stardance_response)

    return reject_reasons

# TODO: create proof videos via python selenium, open github repo, scroll down, open repo files, scroll through them, open demo link, open stardance project page and that is it 