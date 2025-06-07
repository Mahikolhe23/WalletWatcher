import urllib.parse
import urllib
from sqlalchemy import create_engine
from config.config import SERVER , USER, PASSWORD, DRIVER

server = SERVER
user = USER
password = PASSWORD
driver = DRIVER
database = 'wallet_watcher'

def get_connection():
    params = urllib.parse.quote_plus(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password};TrustServerCertificate=yes')
    engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
    return engine

