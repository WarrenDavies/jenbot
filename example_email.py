import os
import json
import yaml
from datetime import datetime
import textwrap
import time

import requests
from dotenv import load_dotenv
from audiorecorder.audio_recorder import AudioRecorder
import imaplib
import smtplib
import email
from email.message import EmailMessage
from email_reply_parser import EmailReplyParser
from email import policy

from sttjenerator.models import registry
from jenbot.core.orchestrator import Orchestrator
 

load_dotenv()
IMAP_SERVER = os.getenv('IMAP_SERVER')
SMTP_SERVER = os.getenv('SMTP_SERVER')
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
PASSWORD = os.getenv('PASSWORD')

def get_unseen_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    mail_ids = messages[0].split()

    emails = []

    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1], policy=policy.default)
                emails.append(msg)

    mail.logout()
    return emails


def send_reply(to_address, subject, body):
    msg = EmailMessage()
    reply_subject = f"Re: {subject}" if "Re:" not in subject else subject
    msg["Subject"] = reply_subject
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_address
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL_ACCOUNT, PASSWORD)
        server.send_message(msg)


def extract_latest_message(body: str) -> str:
    return EmailReplyParser.parse_reply(body)


with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

orchestrator = Orchestrator(core_config)


while True:
    emails = get_unseen_emails()

    for msg in emails:
        sender = msg["From"]
        subject = msg["Subject"]

        # if "Mk1.5" not in subject:
        #     print("Message ignored:")
        #     print(sender)
        #     print(subject)
        #     continue

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    raw_payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body = raw_payload.decode(charset)
                    except (UnicodeDecodeError, LookupError):
                        body = raw_payload.decode(charset, errors='replace')

        else:
            raw_payload = part.get_payload(decode=True)
            charset = part.get_content_charset() or 'utf-8'
            try:
                body = raw_payload.decode(charset)
            except (UnicodeDecodeError, LookupError):
                body = raw_payload.decode(charset, errors='replace')

        body = extract_latest_message(body)
        print(body)
        payload = {
            "conversation_id": sender, 
            "content": body
        }

        response = orchestrator.process(payload)
        send_reply(sender, subject, response)

    time.sleep(30)