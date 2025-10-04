import os
import pandas as pd
from dotenv import load_dotenv

def get_db_infor() -> str:
    '''Trả về alchemy string để kết nối db'''
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_username = os.getenv("DB_USERNAME")
    db_pwd = os.getenv("DB_PASSWORD")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    conn_url = f"postgresql://{db_username}:{db_pwd}@{db_host}:{db_port}/{db_name}"
    return conn_url

def query_db(query: str) -> pd.DataFrame:
    '''Trả về DataFrame của câu lệnh query'''
    conn_url = get_db_infor()
    return pd.read_sql(query, conn_url)

if __name__ == "__main__":
    print(query_db("SELECT * FROM users"))