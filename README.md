# POS System

A Point of Sale (POS) system built with Python and Tkinter, connected to MySQL database.

## Features

1. Login Page
2. Main Dashboard
3. Category CRUD (Create, Read, Update, Delete)
4. Item CRUD with Barcode support
5. Staff CRUD
6. Safe Page (Transaction entry with print functionality)
7. Safe List (Transaction reports)

## Setup

1. Install MySQL server and create a database named 'pos_db'.
2. Install dependencies: `pip install -r requirements.txt`
3. Update database credentials in `pos_system.py` if necessary (default: host='localhost', user='root', password='')
4. Run the database setup: `python pos_system.py` (it will create tables automatically)
5. Run the application: `python pos_system.py`

## Default Login

- Username: admin
- Password: password

## Database Tables

- users: Login credentials
- categories: Product categories
- items: Products with barcode
- staff: Staff members
- safe_transactions: Safe deposits/withdrawals

## Notes

- Ensure MySQL server is running before starting the application.
- The print functionality saves a receipt to a text file.
