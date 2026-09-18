from checks import run_all_checks
from utils import create_rejection_message
from video import create_video
from fiona import get_cert
from slack import app

from slack_bolt.adapter.socket_mode import SocketModeHandler
import argparse
import os
        
parser = argparse.ArgumentParser(description="clank it up 🚀✨ (this is a joke)")

# setup basic review inputs
parser.add_argument("--fiona", type=str, help="Fiona Dashboard Link (if this is present, all other review inputs will be ignored)")
parser.add_argument("--repo", type=str, help="GitHub Repository Link")
parser.add_argument("--readme", type=str, help="Raw README Link")
parser.add_argument("--stardance", type=str, help="Stardance Project Link")
parser.add_argument("--demo", type=str, help="Demo Link")

args = parser.parse_args()

def main():
    if not args.fiona:
        reject_reasons = run_all_checks(args.readme, args.repo, args.demo, args.stardance)

        if len(reject_reasons) != 0:
            reject_message = create_rejection_message(reject_reasons)
            create_video(args.repo, args.stardance, args.demo)
            return reject_message
        else:
            return "All checks passed"
    elif args.fiona:
        cert = get_cert(args.fiona)
        stardance = f"https://stardance.hackclub.com/projects/{cert['externalId']}"

        reject_reasons = run_all_checks(cert['readmeUrl'], cert['repoUrl'], cert['demoUrl'], stardance)

        if len(reject_reasons) != 0:
            reject_message = create_rejection_message(reject_reasons)
            create_video(cert['repoUrl'], stardance, cert['demoUrl'])

            return reject_message

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    #print(main())