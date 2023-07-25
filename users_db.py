import sqlite3
import random

db_filename = 'EcoPlanner/carbon_footprint.db'
table_name = 'users_table'


def create_table():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create the users_table if it doesn't exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users_table (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def add_users(name, password):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users_table WHERE name = ?", (name,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists")
    else:
        # Generate a random user_id for the new user
        user_id = random.randint(1, 1000)

        # Insert the new user into the table
        insert_query = "INSERT INTO users_table (user_id, name, password) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (user_id, name, password))
        conn.commit()
        print(f"New user with ID {user_id} has been created.")

    conn.close()


def check_user_password(username, password):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Retrieve the user with the given username
    cursor.execute("SELECT * FROM users_table WHERE name = ?", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        return user[0]  # Return the user_id
    else:
        return None

    conn.close()


def display():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Retrieve all users from the table
    cursor.execute("SELECT * FROM users_table")
    rows = cursor.fetchall()

    print("**************************************")
    print("User Display: ")
    for row in rows:
        print(row)
    print("**************************************")

    conn.close()


# create_table()

# Example usage:
# add_users('welcome1', 'welcome1')
# check_user_password('welcome1', 'welcome1')
display()

