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

engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')

with footprintEngine.connect() as connection:
    query = "SELECT SUM(carbon_lb) AS sum_value from drives"
    query_result = connection.execute(db.text(query)).fetchall()
    driveLBS = float(pd.DataFrame(query_result)['sum_value'])
    query = "SELECT SUM(carbon_lb) AS sum_value from flights"
    query_result = connection.execute(db.text(query)).fetchall()
    flightLBS = float(pd.DataFrame(query_result)['sum_value'])
    print("Getting DB: \n --------- \n", driveLBS + flightLBS)