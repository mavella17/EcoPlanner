import git
from flask import Flask, jsonify, render_template
from flask import url_for, flash, redirect, request
import pandas as pd
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                           text='This is the home page')


# used with webhooks to update server
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/EcoPlanner')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
