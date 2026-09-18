from slack_bolt import App
from dotenv import load_dotenv
import os

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("review")
def handle_review(say):
    say("ok :thumbsup:")