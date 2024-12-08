import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from random import shuffle

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "app_key"

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    return conn

# Define rows and columns for seating
ROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
COLUMNS = [0, 1 , 2, 3]

# Function to scramble eTicket name & INFOTC4320
def shuffle_word(text):
    new_text = text + "INFOTC4320"
    new_text = list(new_text)
    shuffle(new_text)
    return ''.join(new_text)

'''
Function to generate cost matrix for flights
Input: none
Output: Returns a 12 x 4 matrix of prices
'''
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

# Calculate total cost for all seats reserved
def get_total_sales(sold_seats, cost_matrix):
    total_sales = 0
    for row in range(len(cost_matrix)):
        for col in range(len(cost_matrix[row])):
            if sold_seats[row][col] == 'reserved':
                total_sales += cost_matrix[row][col]

    return total_sales

# Function to get all reserved seats from the database
def get_reserved_seats():
    seating_chart={}
    conn = get_db_connection()

    # Get the seats from db that have been assigned
    seats = conn.execute('SELECT seatRow, seatColumn FROM reservations ORDER BY seatRow, seatColumn').fetchall()        
    taken_seats = set((row, col) for row, col in seats)
 
    for row in ROWS:
        seating_chart[row] = {}
        for column in COLUMNS:
            # Mark the seat as 'taken' if it's in the taken_seats set, otherwise 'available'
            seating_chart[row][column] = 'reserved' if (row, column) in taken_seats else 'open'
    return seating_chart, taken_seats

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Set admin status to false (not logged in)
    admin_status = False

    # Initialize total sales
    total_sales = 0
    seating_chart = {}

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Check for empty inputs
        if not username or not password:
            raise ValueError('Both username and password fields are required.')

        # Validate credentials
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if admin:
            seating_chart, taken_seats = get_reserved_seats()
            # Calculate total sales based on reservations
            cost_matrix = get_cost_matrix()
            total_sales = get_total_sales(seating_chart, cost_matrix)
            # Redirect to reservations with total sales included
            admin_status = True
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('admin.html',admin_status=admin_status, seating_chart=seating_chart, total_sales=total_sales)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
     # Initialize empty success message
    success_message = ""

    # Create lists with selection options
    row_options = [0,1,2,3,4,5,6,7,8,9,10,11]
    seat_options = [0,1,2,3]
    
    seating_chart, taken_seats = get_reserved_seats()
    # Get form data for reservation
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        seat_row = request.form.get('selectRow')
        seat_col = request.form.get('selectSeat')

        # Make sure chosen seat and column aren't null values
        if not seat_row:
            flash("Please select a valid row option.")
        elif not seat_col:
            flash("Please select a valid column option.")
        # Make sure chosen seat isn't already reserved
        elif (int(seat_row), int(seat_col)) in taken_seats:
            flash(f"Row: {seat_row} Seat: {seat_col} is already assigned. Choose again.")
        else:
            # Generate eTicketnumber
            eticket_num = shuffle_word(first_name)

            conn = get_db_connection()
            #insert data into database
            conn.execute('INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES (?, ?, ?, ?)', (first_name, seat_row, seat_col, eticket_num))
            conn.commit()

            # Update seating chart to display newly reserved seat
            seating_chart, taken_seats = get_reserved_seats()
            conn.close()
            success_message = f"Congratulations {first_name}! Row: {seat_row}, Seat: {seat_col} is now reserved for you. Enjoy your trip!\nYour eticket number is: {eticket_num}"
        
    return render_template('reservations.html', seating_chart=seating_chart, row_options=row_options, seat_options=seat_options, success_message=success_message)

# Error handler for displaying ValueError messages
@app.errorhandler(ValueError)
def handle_value_error(e):
    return render_template('admin.html', error_message=str(e)), 400



# route to create a post
app.run(host="0.0.0.0")