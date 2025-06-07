from core.parse_emails import email_parser
from config.db_conn import get_connection
from dateutil.parser import parse
import pandas as pd

def save_trans_to_db():
    conn = get_connection()
    data = email_parser()
    df = pd.DataFrame(data, columns=['date', 'mode', 'amount', 'category'])

    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    df['amount'] = df['amount'].astype(float)
    df['mode'] = df["mode"].astype(str)
    df['category'] = df['category'].astype(str)
    df.to_sql(name='transactions', con=conn, if_exists='append', index=False)


