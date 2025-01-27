import logging

from bot_template import email_utils

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    email_utils.send_email_plain(receiver_email="mikolaj.kardys@gmail.com", subject="Test", body="Email from Python")
