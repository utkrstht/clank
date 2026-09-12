from checks import run_all_checks
from utils import create_rejection_message
import argparse
        
parser = argparse.ArgumentParser(description="clank it up 🚀✨ (this is a joke)")

# setup basic review inputs
parser.add_argument("--repo", type=str, help="GitHub Repository Link")
parser.add_argument("--readme", type=str, help="Raw README Link")
parser.add_argument("--stardance", type=str, help="Stardance Project Link")
parser.add_argument("--demo", type=str, help="Demo Link")

args = parser.parse_args()

def main():
    reject_reasons = run_all_checks(args.readme, args.repo, args.demo)

    if len(reject_reasons) != 0:
        reject_message = create_rejection_message(reject_reasons)
        return reject_message
    else:
        return "All checks passed"

if __name__ == "__main__":
    print(main())