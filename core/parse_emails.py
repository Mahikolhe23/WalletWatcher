import email
import re
import pandas as pd
import pytz

from email.header import decode_header
from bs4 import BeautifulSoup
from core.fetch_emails import get_mails
from dateutil.parser import parse

merchant_to_category = {
    "zomato": "Food",
    "swiggy": "Food",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "cred": "Credit Card Bill",
    "paytm": "Recharge/Wallet",
    "electricity": "Utilities"
}

def get_amount(text):
    matches = re.findall(r'(?:rs\.?|inr|₹|amount|amt)[:\-\s]*([\d,]+(?:\.\d{1,2})?)', text.lower())
    if matches:
        return matches[0].replace(',', '')
    return None

def email_parser():
    mail, email_ids = get_mails()
    columns = ['date', 'mode', 'amount', 'category']
    email_data = pd.DataFrame(columns=columns)

    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)")
        if result == 'OK':
            raw_email = data[0][1]

            msg = email.message_from_bytes(raw_email)
            date_str = msg.get("Date")
            date_object = email.utils.parsedate_to_datetime(date_str)
            ist = pytz.timezone('Asia/Kolkata')
            ist_date_time = date_object.astimezone(ist)

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

        if 'transaction' in email_body.lower():
            amount = get_amount(email_body)
            mode = ''
            category = ''
            print(email_body)
            email_body = email_body.lower()            

            for key, category in merchant_to_category.items():
                if key in email_body:
                    category = merchant_to_category[key]
                    break
                else:
                    continue        

            if "upi" in email_body or "@ybl" in email_body or "@axl" in email_body:
                mode = "UPI"
            elif 'credit card' in email_body:
                mode = "Credit Card"
            elif 'debit card' in email_body:
                mode = "Debit Card"
            elif any(wallet in email_body for wallet in ["phonepe", "paytm", "google pay"]):
                mode = "Wallet"
            else:
                mode = "Bank Transfer"

            email_data = pd.concat([email_data,pd.DataFrame([
                {
                    'date' : ist_date_time,
                    'mode' : mode,
                    'amount' : amount,
                    'category' : category
                }
            ])],ignore_index=True)

    return email_data


