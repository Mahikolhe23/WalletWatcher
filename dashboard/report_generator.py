from config.db_conn import get_connection
import pandas as pd

def generate_report():
    engine = get_connection()
    sql_query = """
                SELECT * FROM transactions
                """
    df = pd.read_sql(sql_query, engine)
    df = df.reset_index(drop=True)
    return df
    



