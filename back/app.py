import socket
import uuid

import uvicorn
import ydb
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

import config
from data_access.comment import Comment
from data_access.comments_repository import CommentsRepository

config = config.parse_config()
connection_string = config["connection_string"]
creds = ydb.iam.ServiceAccountCredentials.from_file(config["creds_file_path"])
comments_repository = CommentsRepository(connection_string, creds)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    with open("./version", "r") as f:
        version = f.readline()
    return {"hostname": socket.gethostname(), "version": version}


@app.get("/_ping")
def ping():
    return "pong"


@app.get("/get-comments")
def get_comments():
    comments = comments_repository.get_comments()
    return {"data": [{"text": x.comment_text, "datetime": x.datetime.ctime(), "username": x.username}
                     for x in comments]}


@app.post("/save-comment")
def save_comment(data=Body()):
    text = data.get("text")
    username = data.get("username")
    entity = Comment(str(uuid.uuid4()), text, ydb.datetime.now(), username)
    comments_repository.save_comment(entity)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
