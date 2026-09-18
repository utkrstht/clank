from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from main import main
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

    fiona = parts[1]
    reject_message = main()
    
    if reject_message:
        say(reject_message) # TODO: handle uploading and sending proof video 


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()