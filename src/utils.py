from pygments.lexer import guess_lexer
from pygments.token import Comment
import unicodedata
import string
import pygments
import time
import ast
import requests
import base64

# Line 6's fstring function was generated via generative AI (being Google AI Overview), search/prompt is "<insert function code from commit 3833b6e> How can I make this shorter?"
def create_rejection_message(rejection_reasons):
    template = f"""Hello, your project has the following issues, please fix them for approval:
{"\n".join(f"- {item}" for item in rejection_reasons)}
If you have any questions, DM @kaboom or create a ticket in #ask-the-shipwrights. """\

    return template

def calculate_ratelimit(response):
    ratelimit_remaining = response.headers.get("X-RateLimit-Reset")
    sleep_time = int(ratelimit_remaining) - time.time() + 5 # 5 is a small buffer

    return sleep_time

def is_banned_domain(demo):
    if "onrender." in demo or "streamlit." in demo or "hf." in demo or "huggingface." in demo or "ngrok" in demo or "cloudflared" in demo or "youtube." in demo or "youtu.be" in demo:
        return True
    else:
        return False

def get_repository_default_branch(repo, headers):
    headers["Accept"] = "application/vnd.github+json"

    response = requests.get(repo, headers=headers)
    response.raise_for_status()

    return response.json().get("default_branch", "main")

def get_repository_tree(repo, branch, headers):
    # https://github.com/example/repository/git/trees/main?recursive=1
    url = f"{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json().get("tree", [])

def get_file(repo, file_sha, headers):
    # https://github.com/example/repository/git/blob/insert_file_sha_lol
    url = f"{repo}/git/blobs/{file_sha}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    if data.get("encoding") == "base64":
        filebytes = base64.b64decode(data.get("content"))
        return filebytes.decode("utf-8", errors="replace")
    return ""

# counts comments for a not known language
def count_comments(content):
    try:
        lexer = guess_lexer(content)
        tokens = pygments.lex(content, lexer)
        comments = 0

        for token_type, token_value in tokens:
            if token_type in Comment or token_type.parent in Comment:
                if token_value.strip():
                    comments += 1

        return comments

    except Exception as e:
        print("whoops. couldn't detect language: ", e)

def count_docstrings(content):
    try:
        tree = ast.parse(content)
        docstrings = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if ast.get_docstring(node) is not None:
                    docstrings += 1

    except SyntaxError as e:
      # print("ouu shii it wasn't python: ", e)
        pass
    except Exception as e:
        print("ouu shii something happened: ", e)

