import sqlalchemy as db
from sqlalchemy import select, create_engine
from sqlalechemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.engine.reflection import Inspector


def users():
    engine = db.create_engine('sqlite:///carbon_footprint.db')
    metadata = MetaData()

    table_name = 'users_table'
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


def add_users():
    name = input("Enter name: ")
    password = input("Enter Password: ")
    trip = input("Trip: ")
    carbon_footprint = float(input("Carbon Footprint: "))

    engine = db.create_engine('sqlite:///carbon_footprint.db')

    metadata = MetaData()
    table_name = 'users_table'
    your_table = Table(
        table_name,
        metadata,
        Column('name', String(255)),
        Column('password', String(255)),
        Column('trip', String(255)),
        Column('carbon_footprint', Float)
    )

    with engine.connect() as connection:
        ins = your_table.insert().values(
            name=name,
            password=password,
            trip=trip,
            carbon_footprint=carbon_footprint
        )
        connection.execute(ins)


def display():
    engine = create_engine('sqlite:///carbon_footprint.db')
    metadata = MetaData()

    table_name = 'users_table'
    your_table = Table(
        table_name,
        metadata,
        Column('name', String(255)),
        # Column('password', String(255))
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

# users() #create the table
# add_users() #This adds the user to the table
display()  # this displays the added users
