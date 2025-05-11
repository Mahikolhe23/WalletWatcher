import pyodbc
from config.config import SERVER , USER, PASSWORD, DRIVER

server = SERVER
user = USER
password = PASSWORD
driver = DRIVER
database = 'wallet_watcher'

def get_connection():
    try:
        connetion = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database}:UID={user};PWD={password};TrustServerCertificate=yes;')
        print('Connection succesfull')
    except Exception as e:
        print(f'Connect failed - {e}')
    conn = connetion.cursor()
    return conn




