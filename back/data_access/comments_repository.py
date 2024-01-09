from typing import List

import ydb.iam
from ydb import BaseSession
from ydb.iam.auth import BaseJWTCredentials

from data_access.comment import Comment


class CommentsRepository:
    def __init__(self, connection_string: str, creds: BaseJWTCredentials):
        self.connection_string = connection_string
        self.creds = creds

    def get_comments(self) -> List[Comment]:
        def callee(session: BaseSession):
            transaction = session.transaction(ydb.SerializableReadWrite())
            result = transaction.execute('select * from comments order by datetime desc limit 5;')
            transaction.rollback()

            return result

        with ydb.Driver(connection_string=self.connection_string, credentials=self.creds) as driver:
            with ydb.SessionPool(driver) as pool:
                query_result = pool.retry_operation_sync(callee)[0].rows
                return [Comment(x.id, x.comment_text, ydb.datetime.fromtimestamp(x.datetime), x.username)
                        for x in query_result]

    def save_comment(self, comment: Comment):
        def callee(session: BaseSession):
            transaction = session.transaction()
            transaction.execute(
                f'''insert into comments (id, comment_text, datetime, username) values (
                "{comment.id}", 
                "{comment.comment_text}",
                DATETIME("{comment.datetime.isoformat(timespec='seconds')}Z"), 
                {f'"{comment.username}"' if comment.username else "null"}
                );'''
            )
            transaction.commit()

        with ydb.Driver(connection_string=self.connection_string, credentials=self.creds) as driver:
            with ydb.SessionPool(driver) as pool:
                pool.retry_operation_sync(callee)


