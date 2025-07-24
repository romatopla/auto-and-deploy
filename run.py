import configparser
from datetime import datetime, timedelta
import pandas as pd
import os
import yfinance as yf
from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read("config.ini")

COMPANIES = eval(config["Companies"]["COMPANIES"])
SALES_PATH = config["Files"]["SALES_PATH"]
DATABASE_CREDS = config['Database']

sales_df = pd.DataFrame( )
if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    os.remove(SALES_PATH)


historical_d = {}
for company in COMPANIES:
    historical_d[company] = yf.download(
        company,
        start=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
        end=datetime.today().strftime("%Y-%m-%d"),
    ).reset_index()

database = PGDatabase(
    host = DATABASE_CREDS['HOST'],
    database = DATABASE_CREDS['DATABASE'],
    user = DATABASE_CREDS['USER'],
    password = DATABASE_CREDS['PASSWORD']
)

for i,row in sales_df.iterrows():
    query = f"insert into sales values ('{row['dt']}','{row['company']}','{row['transaction_type']}',{row['amount']})"
    database.post(query)
for company,data in historical_d.items():
    for i,row in data.iterrows():
        d = row.reset_index()
        query = f"insert into stock  values ('{d[d['Price'] == 'Date'][0].to_numpy()[0].strftime('%Y-%m-%d')}','{d['Ticker'][1]}',{round(d[d['Price'] == 'Open'][0].to_numpy()[0],2)},{round(d[d['Price'] == 'Close'][0].to_numpy()[0],2)})"
        database.post(query)

    