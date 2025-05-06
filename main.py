import requests
import imaplib
import pandas as pd
import email
from dateutil.parser import parse
from email.header import decode_header
from config.gmail_auth import get_token
from bs4 import BeautifulSoup

def extract_first_date(words):
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

def connect_to_gmail():
    creds = get_token()
    access_token = creds.token

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    user_email = user_info.get('email', 'unknown@domain.com')

    # Create the authentication string without base64 encoding
    oauth2_string = f"user={user_email}\x01auth=Bearer {access_token}\x01\x01"

    # Connect to the Gmail IMAP server using SSL
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    columns = ['date', 'tran_type', 'amount']

    try:
        # Authenticate using the XOAUTH2 mechanism
        mail.authenticate('XOAUTH2', lambda x: oauth2_string)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")

        email_ids = []
        df = pd.DataFrame(columns=columns)    
        if result == "OK":
            email_ids = data[0].split()[-20:]
        else:
            print("Search failed:", result)

        for email_id in email_ids:    
            result, data = mail.fetch(email_id, "(RFC822)") 
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            body = ""
            content_type = ""
            
            # Get the body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type in ['text/plain','text/html'] and 'attachment' not in content_disposition:
                        pay_load = part.get_payload(decode=True)
                        if pay_load:
                            body = pay_load.decode(errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')
        
            if msg.get_content_type() == "text/html" or "<html" in body:
                soup = BeautifulSoup(body, "html.parser")
                for script in soup(["script", "style", "img", "a"]):
                    script.extract()
                body = soup.get_text(separator=" ", strip=True)

            if 'transaction' in body.lower() or 'upi' in body.lower():
                body_list = body.split(' ')
                date = extract_first_date(body_list)
                tran_type = get_tran_type(body_list)
                amount = get_amount(body_list)

                df = pd.concat([df,pd.DataFrame([
                    {
                        'date':date,
                        'tran_type':tran_type,
                        'amount':amount
                    }
                ])],ignore_index=True)
        
        print(df)

    except imaplib.IMAP4.error as e:
        print("Authentication Error:", e)

if __name__ == "__main__":
    connect_to_gmail()
