import git
from flask import Flask, jsonify, render_template
from flask import url_for, flash, redirect, request, session
import pandas as pd
from dotenv import load_dotenv
import os
from key import BKEY
import sqlalchemy as db
from sqlalchemy import select
import requests
from sqlalchemy.sql import text as sa_text
from forms import driveData, flightData, registrationData
from flask_behind_proxy import FlaskBehindProxy
from users_db import users, add_users, display

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
load_dotenv()
app.config['SECRET_KEY'] = 'c275b91d07ca2bdd6359'
engine = db.create_engine('sqlite:///EcoPlanner/vehicles.db')
engine = db.create_engine('sqlite:///EcoPlanner/carbon_footprint.db')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                           text='This is the home page')


used with webhooks to update server
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
    form = registrationData()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # add_users(username, password)
        flash(f'Account created for {form.username.data}', 'success!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


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


@app.route('/drive_lookup', methods=['POST'])
def drive_lookup():
    bkey = BKEY
    headers = {
                'Authorization': 'Bearer ' + bkey,
                'Content-Type': 'application/json'
            }
    api = 'https://www.carboninterface.com/api/v1/estimates'
    data = request.get_json()
    req = requests.post(api, headers=headers, json=data)
    return jsonify(req.json())


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    # display()
    app.run(debug=True, host="0.0.0.0", port="6700")
