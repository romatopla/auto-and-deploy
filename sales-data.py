from datetime import datetime,timedelta
import pandas as pd
from random import randint
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

COMPANIES = eval(config['Companies']['COMPANIES'])

today = datetime.today()
yestarday = today - timedelta(days=1)
if 1<=today.weekday():
    d = {
        'dt' : [yestarday.strftime('%m/%d/%Y') ]* len(COMPANIES) * 2,
        'company' : COMPANIES * 2,
        'transaction_type' : ['buy'] * len(COMPANIES) + ['sell'] * len(COMPANIES),
        'amount' : [randint(1,1000) for _ in range(len(COMPANIES) * 2)]
    }
df = pd.DataFrame(d)
df.to_csv('sales_data.csv',index=False)
