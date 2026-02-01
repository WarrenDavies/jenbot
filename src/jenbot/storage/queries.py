import sqlite3
from pydantic import BaseModel

from jenbot.schemas.queries import query_param_schemas

def get_recent_messages():

    query = """
        select role, content
        from (
            SELECT role, content, record_created_time
            FROM messages
            WHERE conversation_id = ?
            ORDER BY record_created_time DESC
            LIMIT ?
        ) as messages
        order by record_created_time asc
    """

    return query