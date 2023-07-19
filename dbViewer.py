import requests
import pandas as pd
import pprint
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text

engine = db.create_engine('sqlite:///vehicles.db')
with engine.connect() as connection:
    query_result = connection.execute(db.text("""SELECT * FROM
    vehicles where year = 2021""")).fetchall()
    print("Getting DB: \n --------- \n",pd.DataFrame(query_result))
