from flask import Flask, request
import json

token="token"
bot = Bot(token, base_url=None, base_file_url=None, request=None)


app = Flask(__name__)

send_channel_list = []

def push(json_msg):
    pass
def commit_comment(json_msg):
    pass
def issues(json_msg):
    pass
def issue_comment(json_msg):
    for chat_id in send_channel_list:
        bot.send_message(chat_id=chat_id, text="text")
def pull_request(json_msg):
    pass
def pull_request_review(json_msg):
    pass
def pull_request_review_comment(json_msg):
    pass

def parse_message(message, event):
    event_list = {
        "push": push,
        "commit_comment": commit_comment,
        "issues": issues,
        "issue_comment": issue_comment,
        "pull_request": pull_request,
        "pull_request_review": pull_request_review,
        "pull_request_review_comment": pull_request_review_comment
    }
    json_msg = json.dumps(message)
    event_list.get(event, lambda: "nothing")(json_msg)

@app.route('/', methods=['GET', 'POST'])
def receive_github_event():
    if request.method == "POST":
        event_name = request.headers.get("X-GitHub-Event")
        parsed_msg = parse_message(request.data.decode("utf-8"), event_name)
    return "Hello World!"

@app.route("/add/<int:chat_id>")
def add_channel(chat_id):
    send_channel_list.append(chat_id)
    return "OK"

@app.route("/bot/<int:chat_id>")
def add_bot(chat_id):
    send_channel_list.append(chat_id)
    return "OK"

def runserver(bot={}):
    bot = bot
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    runserver()

