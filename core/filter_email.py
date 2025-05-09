import pandas as pd
from core.parse_emails import email_parser, get_first_date, get_tran_type, get_amount

def filter_email():
    emails = email_parser()
    columns = ['date', 'tran_type', 'amount']
    email_data = pd.DataFrame(columns=columns)

    for email in emails:
        if 'transaction' in email.lower() or 'upi' in email.lower():
            body_list = email.split(' ')
            date = get_first_date(body_list)
            tran_type = get_tran_type(body_list)
            amount = get_amount(body_list)
            email_data = pd.concat([email_data,pd.DataFrame([
                {
                    'date':date,
                    'tran_type':tran_type,
                    'amount':amount
                }
            ])],ignore_index=True)

    return email_data

