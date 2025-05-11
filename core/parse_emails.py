import email
import re
import pandas as pd
import pytz
from email.header import decode_header
from bs4 import BeautifulSoup
from core.fetch_emails import get_mails
from dateutil.parser import parse

transactions_keys = ["debited", "credited", "spent", "received", "UPI", "transaction", "payment"]

merchant_to_category = {
    "zomato": "Food",
    "swiggy": "Food",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "cred": "Credit Card Bill",
    "paytm": "Recharge/Wallet",
    "electricity": "Utilities"
}

payment_category = {
    "upi" : "UPI",
    "credit card" : "Credit Card",
    "debit card" : "Debit Card"
}

def get_amount(email):
    matches = re.findall(r'(?:rs\.?|inr|₹|amount|amt)[:\-\s]*([\d,]+(?:\.\d{1,2})?)', email.lower())
    if matches:
        return matches[0].replace(',', '')
    return None

def get_category(email):
    category = ''   
    for key, category in merchant_to_category.items():
        if key in email:
            category = merchant_to_category[key]
            break
        else:
            continue        
    return category            

def get_mode(email):
    mode = ''    
    for key , mode in payment_category.items():
        if key in email:
            mode = payment_category[key]
            break
        else:
            continue
    return mode        

def extract_email_body(raw_msg):
    email_body = ''    
    if raw_msg.is_multipart():
        for part in raw_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type in ['text/plain','text/html'] and 'attachment' not in content_disposition:
                pay_load = part.get_payload(decode=True)
                if pay_load:
                    email_body = pay_load.decode(errors='ignore')
    else:
        email_body = raw_msg.get_payload(decode=True).decode(errors='ignore')

    if raw_msg.get_content_type() == "text/html" or "<html" in email_body:
        soup = BeautifulSoup(email_body, "html.parser")
        for script in soup(["script", "style", "img", "a"]):
            script.extract()
        email_body = soup.get_text(separator=" ", strip=True)
    return email_body

def extract_transaction_details(email_body):
    email_body = email_body.lower()
    if not any(key in email_body for key in transactions_keys):
        return None

    return { 
        'mode' : get_mode(email_body),
        'amount' : get_amount(email_body),
        'category' : get_category(email_body)
    }


def email_parser():
    mail, email_ids = get_mails()
    data = []
    for email_id in email_ids:
        result, fetch_data = mail.fetch(email_id, "(RFC822)")
        if result != 'OK':
            continue

        raw_email = fetch_data[0][1]
        raw_msg = email.message_from_bytes(raw_email)

        try:
            date_str = raw_msg.get("Date")
            date_object = email.utils.parsedate_to_datetime(date_str)
            email_date = date_object.astimezone(pytz.timezone('Asia/Kolkata'))
        except:
            continue

        subject, encoding = decode_header(raw_msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        email_body = extract_email_body(raw_msg)
        transactions = extract_transaction_details(email_body)

        if transactions:
            data.append({
                'date':email_date,
                **transactions
            })

    return pd.DataFrame(data, columns=['date', 'mode', 'amount', 'category'])


