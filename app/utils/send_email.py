from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS")
)


# Sending email


def send_email(subject: str, recipient: list, message: str, background_tasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype='plain'
    )

    fm = FastMail(conf)
    # await fm.send_message(message)
    background_tasks.add_task(fm.send_message, message)
    print("====================")
