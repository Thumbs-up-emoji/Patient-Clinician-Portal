import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'zero'),
        password=os.getenv('DB_PASSWORD','SixNine_420'),
        database=os.getenv('DB_NAME', 'patient_portal'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection