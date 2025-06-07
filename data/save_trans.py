from core.parse_emails import email_parser
from config.db_conn import get_connection

def save_trans_to_db():
    email_data = email_parser()
    conn = get_connection()

    sql_query = """
                
                """



