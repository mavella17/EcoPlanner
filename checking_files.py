import sqlalchemy as db
from sqlalchemy import select, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.engine.reflection import Inspector

# Function to display the data in a table
def display_table_data(table_name):
    engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
    metadata = MetaData()

    # Define the table based on the table_name
    if table_name == 'drives':
        your_table = Table(
            'drives',
            metadata,
            autoload=True,
            autoload_with=engine
        )
    elif table_name == 'flights':
        your_table = Table(
            'flights',
            metadata,
            autoload=True,
            autoload_with=engine
        )
    elif table_name == 'users_table':
        your_table = Table(
            'users_table',
            metadata,
            autoload=True,
            autoload_with=engine
        )
    else:
        print(f"Table '{table_name}' does not exist.")
        return

    # Connect to the database and fetch all rows from the table
    with engine.connect() as conn:
        select_query = your_table.select()
        result = conn.execute(select_query)
        rows = result.fetchall()

        # Print the data
        print(f"Data in table '{table_name}':")
        for row in rows:
            print(row)
        print("**************************************")
def get_columns(table_name):
    engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    return table.columns.keys()

def add_user_id_column():
    engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
    with engine.connect() as conn:
        # Add the 'user_id' column to the 'drives' table
        alter_table_query = "ALTER TABLE flights ADD COLUMN user_id INTEGER;"
        conn.execute(alter_table_query)

#add_user_id_column()
#columns = get_columns('flights')
#print("Columns in 'flights' table:", columns)
