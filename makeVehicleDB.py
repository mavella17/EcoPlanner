import requests
import pandas as pd
import pprint
import sqlalchemy as db
from sqlalchemy import select
import os
from sqlalchemy.sql import text as sa_text

b = os.environ.get('BEARER_KEY')
header = {'Authorization': 'Bearer ' + b}
url = 'https://www.carboninterface.com/api/v1/vehicle_makes'
req = requests.get(url, headers=header)
# pprint.pprint(req.json())\
makes = {}
for data in req.json():
    make = data['data']
    makes[data['data']['attributes']['name']] = data['data']['id']
dfs = []
for key in makes:
    url = 'https://www.carboninterface.com/api/v1/vehicle_makes/'
    url += makes[key]
    url += '/vehicle_models'
    req = requests.get(url, headers=header)
    cars = req.json()
    for car in cars:
        data = car['data']
        df = pd.DataFrame(data['attributes'], index=[0])
        df['id'] = data['id']
        df['type'] = data['type']
        df = df.drop('type', axis=1)
        dfs.append(df)
combined_df = pd.concat(dfs, axis=0)
engine = db.create_engine('sqlite:///vehicles.db')
combined_df.to_sql('vehicles', con=engine, if_exists='replace', index=True)
with engine.connect() as connection:
    query_result = connection.execute(db.text("""SELECT * FROM
    vehicles""")).fetchall()
    print("Getting DB: \n --------- \n", pd.DataFrame(query_result))
