import git
from flask import Flask, jsonify, render_template, logging
from flask import url_for, flash, redirect, request, session
import pandas as pd
from dotenv import load_dotenv
import os
import flask_login
import flask
from key import BKEY
import sqlalchemy as db
import pprint
import sqlite3
import random
from sqlalchemy import select, MetaData, Table
import requests
from sqlalchemy.sql import text as sa_text
from forms import driveData, flightData, registrationData, loginData
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
load_dotenv()
app.config['SECRET_KEY'] = 'c275b91d07ca2bdd6359'
engine = db.create_engine('sqlite:///EcoPlanner/vehicles.db')
footprintEngine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# users = {'admin@gmail.com': {'password': 'pass'}}

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
conn.commit()


def register_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_exist = cursor.fetchone()

    if user_exist:
        print("account already exist")
    else:
        user_id = random.randint(1, 1000)
        sq = "INSERT INTO users (user_id, email, password) VALUES (?, ?, ?)"
        cursor.execute(sq, (user_id, email, password))
        conn.commit()
        print(f"New user with ID {user_id} has been created.")

        conn.close()


def display():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print('Display: ')
    for row in rows:
        print(row)
    conn.close()


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_obj = User()
        user_obj.id = email
        return user_obj


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not email:
        return None

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User()
        user.id = user_data[1]
        return user

    return None


@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                           text='This is the home page')


# used with webhooks to update server
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/EcoPlanner/EcoPlanner')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route("/drive", methods=['GET', 'POST'])
def drive_data():
    form = driveData()
    if form.validate_on_submit():
        return redirect(url_for('results'))
    return render_template('drive.html', title='Drive Data', form=form)


@app.route('/flights', methods=['GET', 'POST'])
def flight_data():
    form = flightData()
    if form.validate_on_submit():
        return redirect(url_for('results'))
    return render_template('flights.html', title='Flight Data', form=form)


@app.route("/register", methods=['GET', 'POST'])
def registration_Data():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        register_user(email, password)
        flash(f'Account created for {email}', 'success!')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user and password == user[2]:
        user_obj = User()
        user_obj.id = email
        flask_login.login_user(user_obj)
        flash(f'Logged in successfully as {email}', 'success!')
        return redirect(url_for('home'))

    flash('Error: Invalid email or password.', 'danger')
    return redirect(url_for('login'))


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route("/check_login_status")
def check_login_status():
    if flask_login.current_user.is_authenticated:
        return jsonify({"status": "logged_in",
                        "user": flask_login.current_user.id})
    else:
        return jsonify({"status": "not_logged_in"})


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/get_models', methods=['POST'])
def get_options():
    selected_value = request.form['selected_value']
    query = "SELECT distinct name FROM vehicles WHERE vehicle_make = '"
    query += str(selected_value) + "';"
    with engine.connect() as connection:
        query_result = connection.execute(db.text(query)).fetchall()
    return jsonify(options=[item[0] for item in query_result])


@app.route('/get_years', methods=['POST'])
def get_years():
    selected_value = request.form['selected_value']
    query = "SELECT distinct year, id FROM vehicles WHERE name = '"
    query += str(selected_value) + "';"
    with engine.connect() as connection:
        query_result = connection.execute(db.text(query)).fetchall()
    return jsonify(options=[(item[0], item[1]) for item in query_result])


@app.route('/clearFlights', methods=['GET'])
def clearFlights():
    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        query = "DELETE FROM flights WHERE user_id = '" + user_id + "';"
        with footprintEngine.begin() as connection:
            connection.execute(db.text(query))
        resp = jsonify(success=True)
        return resp
    return jsonify({"message": "Authentication required."}), 401


@app.route('/clearDrives', methods=['GET'])
def clearDrives():
    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        query = "DELETE FROM drives WHERE user_id = '" + user_id + "';"
        with footprintEngine.begin() as connection:
            connection.execute(db.text(query))
        resp = jsonify(success=True)
        return resp
    return jsonify({"message": "Authentication required."}), 401


@app.route('/lookup', methods=['POST'])
def lookup():
    headers = {
        'Authorization': 'Bearer ' + BKEY,
        'Content-Type': 'application/json'
    }
    api = 'https://www.carboninterface.com/api/v1/estimates'
    data = request.get_json()
    req = requests.post(api, headers=headers, json=data)
    if req.status_code >= 200 and req.status_code < 300:
        if data['type'] == 'vehicle':
            row = req.json()['data']['attributes']
            df = pd.DataFrame(row, index=[0])
            if flask_login.current_user.is_authenticated:
                df['user_id'] = flask_login.current_user.id
                df.to_sql('drives', con=footprintEngine,
                          if_exists='append', index=True)
        else:
            row = req.json()['data']['attributes']
            df = pd.DataFrame(row, index=[0])
            temp = pd.DataFrame(df['legs'][0], index=[0])
            df.drop('legs', axis=1, inplace=True)
            result_df = pd.concat([df, temp], axis=1)
            if flask_login.current_user.is_authenticated:
                result_df['user_id'] = flask_login.current_user.id
                result_df.to_sql('flights', con=footprintEngine,
                                 if_exists='append', index=True)

    return jsonify(req.json())


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/poundsCO2')
def poundsCO2():
    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        with footprintEngine.connect() as connection:
            query = "SELECT SUM(carbon_lb) from drives "
            query += "where user_id = '" + user_id + "';"
            drivelbs = connection.execute(db.text(query)).fetchall()[0][0]
            if not drivelbs:
                drivelbs = 0
            query = "SELECT SUM(carbon_lb) from flights "
            query += "where user_id = '" + user_id + "';"
            flightlbs = connection.execute(db.text(query)).fetchall()[0][0]
            if not flightlbs:
                flightlbs = 0
        return jsonify({"flight": flightlbs, "drive": drivelbs})
    return jsonify({"flight": 0, "drive": 0})


@app.route('/getFlights')
def getFlights():

    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        with footprintEngine.connect() as connection:
            query = "SELECT * from flights WHERE user_id = :user_id"
            df = pd.read_sql(query, con=footprintEngine,
                             params={'user_id': user_id})
            results = df.to_dict('records')
            print("FLIGHTS _____", results)
            for record in results:
                record['Date'] = record.pop(
                                 'estimated_at').replace("T", ": ")[:-5]
                if 'index' in record:
                    del record['index']
                if 'carbon_g' in record:
                    del record['carbon_g']
                if 'carbon_kg' in record:
                    del record['carbon_kg']
        return jsonify(results)
    return jsonify([])


@app.route('/getDrives')
def getDrives():
    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        with footprintEngine.connect() as connection:
            query = "SELECT * from drives WHERE user_id = :user_id"
            df = pd.read_sql(query, con=footprintEngine,
                             params={'user_id': user_id})
        results = df.to_dict('records')
        print("FLIGHTS _____", results)
        for record in results:
            record['Date'] = record.pop('estimated_at').replace("T", ": ")[:-5]
            if 'index' in record:
                del record['index']
            if 'carbon_g' in record:
                del record['carbon_g']
            if 'carbon_kg' in record:
                del record['carbon_kg']
            if 'vehicle_model_id' in record:
                del record['vehicle_model_id']
        return jsonify(results)
    else:
        return jsonify([])


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
