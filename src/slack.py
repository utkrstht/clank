from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from main import main
import os

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("!review")
def handle_review(say):
    say("ok :thumbsup:")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()