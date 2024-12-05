DROP TABLE IF EXISTS reservations;

-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Create seating_chart table
CREATE TABLE IF NOT EXISTS seating_chart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seat_number TEXT NOT NULL,
    reserved_by TEXT
);

-- Create reservations table
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sales INTEGER NOT NULL
);

-- Insert sample admin data
INSERT INTO admins (username, password) VALUES ('admin', 'password123');

-- Insert sample seating chart data
INSERT INTO seating_chart (seat_number, reserved_by) 
VALUES ('A1', 'John Doe'), 
       ('A2', 'Jane Doe');

-- Insert sample reservation sales data
INSERT INTO reservations (sales) 
VALUES (100), 
       (150);