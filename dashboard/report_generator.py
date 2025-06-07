from config.db_conn import get_connection
import pandas as pd

def generate_report():
    engine = get_connection()
    sql_query = """
                SELECT * FROM transactions WHERE amount = '250'
                """
    df = pd.read_sql(sql_query, engine)
    return df
    



