from core.parse_emails import email_parser
from config.db_conn import get_connection

def save_trans_to_db():
    email_data = email_parser()
    conn = get_connection()

    sql_query = """
                    IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'wallet_watcher')
                    BEGIN
                        CREATE DATABASE wallet_watcher
                    END
                    GO

                    USE wallet_watcher
                    GO

                    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'transactions')
                    BEGIN
                        CREATE TABLE transactions(
                            trans_id INT IDENTITY(1,1) ,
                            trans_date DATETIME ,
                            trans_mode VARCHAR(20) ,
                            trans_amount FLOAT ,
                            trans_category VARCHAR(30)
                        )
                    END
                    GO
                """

    conn.execute(sql_query)

    sql_query = """
                    INSERT INTO transactions(trans_date, trans_mode, trans_amount, trans_category)
                    VALUES
                """


