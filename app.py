import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True



# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/admin')
def admin():
    
    return render_template('admin.html')

@app.route('/reservations')
def reservations():
    
    return render_template('reservations.html')


# route to create a post
app.run()