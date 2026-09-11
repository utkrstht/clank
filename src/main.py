import argparse
import re

# holy shit
RAW_README_REGEX = r"^https?:\/\/(?:raw\.githubusercontent\.com\/[^\/]+\/[^\/]+\/[^\/]+|gitlab\.com\/api\/v4\/projects\/[^\/]+\/repository\/files\/README(?:\.[a-zA-Z0-9]+)?\/raw|bitbucket\.org\/[^\/]+\/[^\/]+\/raw\/[^\/]+)\/README(?:\.[a-zA-Z0-9]+)?$"

# TODO: add all possible rejection reasons to dictionary 

parser = argparse.ArgumentParser(description="clank it up 🚀✨ (this is a joke)")

# setup basic review inputs
parser.add_argument("--repo", type=str, help="GitHub Repository Link")
parser.add_argument("--readme", type=str, help="Raw README Link")
parser.add_argument("--stardance", type=str, help="Stardance Project Link")
parser.add_argument("--demo", type=str, help="Demo Link")

args = parser.parse_args()

# raw readme check
if re.match(RAW_README_REGEX, args.readme, re.IGNORECASE):
    pass # TODO: create rejection message based on all checks done