import requests
import imaplib
from dateutil.parser import parse
from config.gmail_auth import *

def get_first_date(words):
    for word in words:
        try:
            word = word.strip(".,;:")  
            dt = parse(word, dayfirst=True, fuzzy=False)
            return dt
        except:
            continue
    return None

def get_tran_type(trans):
    tran = None    
    for t in trans:
        if 'debit' in t.lower():
            tran = 'Debit'
        if 'credit' in t.lower():
            tran = 'Credit'
    return tran

def get_amount(trans):
    amount = None    
    for a in trans:
        if 'rs.' in a.lower():
            amount = f'{a}'
    return amount

def get_mails():
    creds = get_token()
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

        result, data = mail.search(None, "ALL")

        email_ids = []
        if result == "OK":
            email_ids = data[0].split()[-2:]
        else:
            print("Search failed:", result)
    except imaplib.IMAP4.error as e:
        print("Authentication Error:", e)

    return mail, email_ids

