import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailServiceSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailServiceSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.sender_email = os.getenv('BOT_EMAIL')
        self.sender_password = os.getenv('BOT_EMAIL_PASSWORD')

        if not self.sender_email or not self.sender_password:
            logging.error("Missing email credentials. Please check your environment variables.")
            raise ValueError("BOT_EMAIL or BOT_EMAIL_PASSWORD is not set.")


def send_email_plain(receiver_email, subject, body):
    logger = logging.getLogger()

    email_service = EmailServiceSingleton()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = email_service.sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_service.sender_email, email_service.sender_password)
        text = msg.as_string()
        server.sendmail(email_service.sender_email, receiver_email, text)
        server.quit()
        logger.info(f"Plaintext email sent to {receiver_email}")
    except smtplib.SMTPException as smtp_error:
        logger.error(f"SMTP error occurred: {smtp_error}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
