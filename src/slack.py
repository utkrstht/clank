from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from checks import run_all_checks
from utils import create_rejection_message
from video import create_video
from fiona import get_cert
import os

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("!review")
def handle_review(message, say):
    say("ok :thumbsup:")
    text = message["text"]
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        say("yo ass forgot the link :joy:")
        return

    fiona = parts[1].strip("<>")

    if "…" in fiona or "..." in fiona:
        say("Link is truncated. Paste the full URL.")
        return

    try:
        cert = get_cert(fiona)
    except Exception as e:
        say(f"Failed to fetch cert: {e}")
        return

    stardance = f"https://stardance.hackclub.com/projects/{cert['externalId']}"

    reject_reasons = run_all_checks(cert['readmeUrl'], cert['repoUrl'], cert['demoUrl'], stardance)

    if len(reject_reasons) != 0:
        reject_message = create_rejection_message(reject_reasons)
        say(reject_message) # TODO: handle uploading and sending proof video
    else:
        say("good boy project")

# shut the fuck up useless console output
@app.event("message")
def handle_message_events():
    pass
    

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()