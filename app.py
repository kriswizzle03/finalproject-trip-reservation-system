import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "app_key"



# use the app.route() decorator to create a Flask view function called index()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_choice = request.form.get('option')
        if user_choice == "reserve_seat":
            return redirect(url_for("reservations"))
        elif user_choice == "admin_login":
            return redirect(url_for("admin"))
        else:
            flash("Please select a valid option.")
            return redirect(url_for("index"))
    return render_template('index.html')

@app.route('/admin')
def admin():
    
    return render_template('admin.html')

@app.route('/reservations')
def reservations():
    
    return render_template('reservations.html')


# route to create a post
app.run()