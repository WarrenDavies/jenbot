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
        ) as recent
        order by record_created_time asc
    """

    return query


def get_conversation_ids():

    query = """
        select conversation_id, latest_message_ts, message_count
        from (
            SELECT conversation_id, max(record_created_time) latest_message_ts, count(conversation_id) message_count -- row_number() over (partition by conversation_id order by record_created_time desc) rn
            FROM messages
            group by conversation_id
        ) as recent
        order by latest_message_ts desc
    """

    return query