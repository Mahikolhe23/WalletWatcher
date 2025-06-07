import email
import re
import pytz
from email.header import decode_header
from bs4 import BeautifulSoup
from core.fetch_emails import get_mails
from rapidfuzz import process, fuzz
from core.email_categorizer import EmailAutoCategorizer

transactions_keys = ["debited", "credited", "spent", "received", "UPI", "transaction", "payment"]

merchant_to_category = {
    "zomato": "Food",
    "swiggy": "Food",
    "uber": "Transport",
    "ola": "Transport",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "paytm": "UPI",
    "google pay": "UPI",
    "gpay": "UPI",
    "phonepe": "UPI",
    "electricity": "Utilities",
    "bescom": "Utilities",
    "cred": "Credit Card Bill",
    "hdfc bank": "Bank",
    "axis bank": "Bank",
    "icici": "Bank",
    "groww":"Investment",
    "zerodha":"Investment",
    "SBI":"Bank",
    "coindcx":"Investment"
}

payment_category = {
    "via upi": "UPI",
    "upi": "UPI",
    "credit card": "Credit Card",
    "debit card": "Debit Card",
    "net banking": "Net Banking",
    "wallet": "Wallet",
    "cash": "Cash"
}

def get_amount(email):
    matches = re.findall(r'(?:rs\.?|inr|₹|amount|amt)[:\-\s]*([\d,]+(?:\.\d{1,2})?)', email.lower())
    if matches:
        return matches[0].replace(',', '')
    return None

def get_category(email):
    best_match = process.extractOne(
        email.lower(),
        merchant_to_category.keys(),
        scorer=fuzz.partial_ratio
    )   
    if best_match and best_match[1] > 80:
        return merchant_to_category[best_match[0]]            

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

    parser = EmailAutoCategorizer()
    result = parser.predict(email_body)
    amount = get_amount(email_body)
    mode = result['mode']
    category = result['category']

    if amount is not None:
        transactions_details = {
        'mode' : mode,
        'amount' : amount,
        'category' : category
        }
        return transactions_details
    else:
        return None

def retrain():
    parser = EmailAutoCategorizer()
    parser._train()

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
    return data


