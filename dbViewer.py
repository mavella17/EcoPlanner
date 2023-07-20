import requests
import pandas as pd
import pprint
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text

# engine = db.create_engine('sqlite:///vehicles.db')
# with engine.connect() as connection:
#     query_result = connection.execute(db.text("""SELECT distinct name FROM
#     vehicles where vehicle_make ='Acura'""")).fetchall()
#     print("Getting DB: \n --------- \n",pd.DataFrame(query_result))
#     print([item[0] for item in query_result])

engine = db.create_engine('sqlite:///vehicles.db')
selected_value = 'Acura'
query = "SELECT * FROM vehicles where name = 'Integra';"
with engine.connect() as connection:
    query_result = connection.execute(db.text(query)).fetchall()
    print("Getting DB: \n --------- \n",pd.DataFrame(query_result))
