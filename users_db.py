import sqlalchemy as db
from sqlalchemy import select, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.engine.reflection import Inspector

table_name = 'users_table'

def users():
    engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
    metadata = MetaData()

    your_table = Table(
        table_name,
        metadata,
        Column('name', String(255)),
        Column('password', String(255)),
        Column('trip', String(255)),
        Column('carbon_footprint', Float)
    )
    inspector = Inspector.from_engine(engine)
    if not inspector.has_table(table_name):
        print(f"Table '{table_name}' does not exist.")
        metadata.create_all(engine)
    else:
        print(f"Table '{table_name}' exists in the database.")


def add_users(name, password):

    engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')

    metadata = MetaData()
    your_table = Table(
        table_name,
        metadata,
        Column('name', String(255)),
        Column('password', String(255)),
        Column('trip', String(255)),
        Column('carbon_footprint', Float)
    )
    with engine.connect() as connection:
        existing_user = connection.execute(select([your_table]).where(your_table.c.name == name)).fetchone()
        if existing_user:
            print("Username already exists")
            return
        ins = your_table.insert().values(
            name=name,
            password=password,
        )
        connection.execute(ins)
    

def display():
    engine = create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
    metadata = MetaData()

    your_table = Table(
        table_name,
        metadata,
        Column('name', String(255)),
        # Column('password', String(255)),
        Column('trip', String(255)),
        Column('carbon_footprint', Float)
    )

    with engine.connect() as conn:
        select_query = your_table.select()
        result = conn.execute(select_query)
        rows = result.fetchall()
        print("**************************************")
        print("User Display: ")
        for row in rows:
            print(row)
        print("**************************************")


# users() 
# add_users()
# display()
