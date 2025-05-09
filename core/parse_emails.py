import email
from email.header import decode_header
from bs4 import BeautifulSoup
from core.fetch_emails import get_mails
from dateutil.parser import parse

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

def email_parser():
    mail, email_ids = get_mails()
    email_bodies = []
    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)") 
        if result == 'OK':
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        email_body = ''    
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type in ['text/plain','text/html'] and 'attachment' not in content_disposition:
                    pay_load = part.get_payload(decode=True)
                    if pay_load:
                        email_body = pay_load.decode(errors='ignore')
        else:
            email_body = msg.get_payload(decode=True).decode(errors='ignore')
    
        if msg.get_content_type() == "text/html" or "<html" in email_body:
            soup = BeautifulSoup(email_body, "html.parser")
            for script in soup(["script", "style", "img", "a"]):
                script.extract()
            email_body = soup.get_text(separator=" ", strip=True)

        if email_body:
            email_bodies.append(email_body)    

    return email_bodies


