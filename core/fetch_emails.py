import requests
import imaplib
from datetime import datetime, timedelta
from config.gmail_auth import get_token

def get_mails(user_name):
    creds = get_token(user_name)
    access_token = creds.token

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    user_email = user_info.get('email', 'unknown@domain.com')

    oauth2_string = f"user={user_email}\x01auth=Bearer {access_token}\x01\x01"

    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        mail.authenticate('XOAUTH2', lambda x: oauth2_string)
        mail.select("inbox")

        yesterday = (datetime.today() - timedelta(days=15)).strftime('%d-%b-%Y')
        today = datetime.today().strftime('%d-%b-%Y')

        result, data = mail.search(None, f'(SINCE "{today}")')

        email_ids = []
        if result == "OK":
            email_ids = data[0].split()
        else:
            print("Search failed:", result)
    except imaplib.IMAP4.error as e:
        print("Authentication Error:", e)

    return mail, email_ids

