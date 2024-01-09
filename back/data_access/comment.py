import ydb


class Comment:
    def __init__(self, id: str, comment_text: str, datetime: ydb.datetime, username=None):
        self.username = username
        self.datetime = datetime
        self.comment_text = comment_text
        self.id = id

    def __str__(self):
        return f'id: {self.id}; comment_text: {self.comment_text}; datetime: {self.datetime}; username:'
