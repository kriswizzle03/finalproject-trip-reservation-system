import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Check for empty inputs
        if not username or not password:
            raise ValueError('Both username and password fields are required.')

        # Validate credentials
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ? AND password = ?', 
                              (username, password)).fetchone()
        conn.close()

        if admin:
            # Redirect to reservations with total sales included
            return redirect(url_for('reservations', show_sales=True))
        else:
            raise ValueError('Invalid username or password. Please try again.')

    return render_template('admin.html')

@app.route('/reservations')
def reservations():
    show_sales = request.args.get('show_sales', default=False, type=bool)

    conn = get_db_connection()
    seating_chart = conn.execute('SELECT * FROM seating_chart').fetchall()

    # Include total_sales only if show_sales is True
    total_sales = None
    if show_sales:
        total_sales = conn.execute('SELECT SUM(sales) as total FROM reservations').fetchone()
    conn.close()

    return render_template('reservations.html', seating_chart=seating_chart, total_sales=total_sales['total'] if total_sales else None)

# Error handler for displaying ValueError messages
@app.errorhandler(ValueError)
def handle_value_error(e):
    return render_template('admin.html', error_message=str(e)), 400

if __name__ == '__main__':
    app.run()