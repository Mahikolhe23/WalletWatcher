import pandas as pd
import email
import pandas as pd
from email.header import decode_header
from bs4 import BeautifulSoup
from utility.utility import *

def connect_to_gmail():
    mail, email_ids = get_mails()
    body = ""
    content_type = ""
    columns = ['date', 'tran_type', 'amount']
    df = pd.DataFrame(columns=columns)
    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)") 
        if result == 'OK':
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        
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
            date = get_first_date(body_list)
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

if __name__ == "__main__":
    connect_to_gmail()
