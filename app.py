import git
from flask import Flask, jsonify, render_template
from flask import url_for, flash, redirect, request, session
import pandas as pd
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
from forms import driveData, flightData
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'c275b91d07ca2bdd6359'

@app.route("/")
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


def get_options_from_database(selected_value):
    
    with engine.connect() as connection:
        query_result = connection.execute(db.text(query)).fetchall()
    return [item[0] for item in query_result]


@app.route('/get_models', methods=['POST'])
def get_options():
    engine = db.create_engine('sqlite:///vehicles.db')
    
    selected_value = request.form['selected_value']
    query = "SELECT distinct name FROM vehicles WHERE vehicle_make = '"
    query += str(selected_value) + "';"
    with engine.connect() as connection:
        query_result = connection.execute(db.text(query)).fetchall()
    return jsonify(options=[item[0] for item in query_result])

@app.route('/get_years', methods=['POST'])
def get_years():
    engine = db.create_engine('sqlite:///vehicles.db')
    selected_value = request.form['selected_value']
    query = "SELECT distinct year FROM vehicles WHERE name = '"
    query += str(selected_value) + "';"
    with engine.connect() as connection:
        query_result = connection.execute(db.text(query)).fetchall()
    return jsonify(options=[item[0] for item in query_result])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
