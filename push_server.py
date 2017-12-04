from flask import Flask, request
from configparser import ConfigParser
from telegram import ParseMode
import json
import telegram

config = ConfigParser()
config.read_file(open("config.ini"))

token = config["DEFAULT"]["token"]
port = config["DEFAULT"]["port"]
parsed_list = config["ROOMID"]["list"][1:-1].replace("\'", "").split(",")
send_channel_list = parsed_list
bot = telegram.Bot(token=token)

app = Flask(__name__)


def push(json_msg):
    msg = "`[{branch}]` New commit pushed by {username}\n".format(
                branch=json_msg["ref"][json_msg["ref"].rindex("/")+1:],
                username=json_msg["pusher"]["name"])
    for commit in json_msg["commits"]:
        msg += "[{commit_id}]({commit_url}) | {commit_message}\n".format(
                commit_id=commit["id"][0:7],
                commit_url=commit["url"],
                commit_message=commit["message"])

    # Send the message
    for chat_id in send_channel_list:
        bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def commit_comment(json_msg):
    repo_json = json_msg["repository"]
    comment_json = json_msg["comment"]
    msg = "New commit comment from `[{repository}]` written by {username}\n".format(
                repository=repo_json["name"],
                username=comment_json["user"]["login"])
    msg += "[{commit_number}]({comment_url}) | {comment_body}\n".format(
                commit_number=comment_json["commit_id"][0:7],
                comment_url=comment_json["html_url"],
                comment_body=comment_json["body"][:30]+"..."
                             if len(comment_json["body"]) > 30
                             else comment_json["body"])

    # Send the message
    for chat_id in send_channel_list:
        bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def issues(json_msg):
    issue_json = json_msg["issue"]
    if json_msg["action"] != "opened":
        return
    repo_json = json_msg["repository"]
    msg = "New issue from `[{repository}]` written by {username}\n".format(
                repository=repo_json["name"],
                username=issue_json["user"]["login"])
    msg += "[#{issue_number}]({issue_url}) | {issue_title}\n".format(
                issue_number=issue_json["number"],
                issue_url=issue_json["html_url"],
                issue_title=issue_json["title"])

    # Send the message
    for chat_id in send_channel_list:
        bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def issue_comment(json_msg):
    issue_json = json_msg["issue"]
    repo_json = json_msg["repository"]
    comment_json = json_msg["comment"]
    msg = "New issue comment from `[{repository}]` written by {username}\n".format(
                repository=repo_json["name"],
                username=issue_json["user"]["login"])
    msg += "[#{issue_number}]({comment_url}) | {comment_body}\n".format(
                issue_number=issue_json["number"],
                comment_url=comment_json["html_url"],
                comment_body=comment_json["body"][:30]+"..."
                             if len(comment_json["body"]) > 30
                             else comment_json["body"])

    # Send the message
    for chat_id in send_channel_list:
        print(chat_id)
        bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


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
    json_msg = json.loads(message)
    event_list.get(event, lambda: "nothing")(json_msg)


@app.route('/', methods=['GET', 'POST'])
def receive_github_event():
    if request.method == "POST":
        event_name = request.headers.get("X-GitHub-Event")
        parsed_msg = parse_message(request.data.decode("utf-8"), event_name)
    return "Hello World!"


@app.route("/add/<chat_id>")
def add_channel(chat_id):
    if request.remote_addr != "127.0.0.1":
        return "Not localhost"
    if chat_id not in send_channel_list:
        send_channel_list.append(str(chat_id))
        print(send_channel_list)
        config.set('ROOMID', 'list', str(send_channel_list))
        config.write(open("config.ini", "w"))
    return "OK"


@app.route("/remove/<chat_id>")
def remove_channel(chat_id):
    if request.remote_addr != "127.0.0.1":
        return "Not localhost"
    if str(chat_id) not in send_channel_list:
        return "Not in list"
    else:
        del send_channel_list[send_channel_list.index(str(chat_id))]
        config.set('ROOMID', 'list', str(send_channel_list))
        config.write(open("config.ini", "w"))
    return "OK"


def runserver(bot={}):
    bot = bot
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    runserver()

