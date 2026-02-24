import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = None
        self.setup_database()  # Ensure DB exists before connect()
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="hidecard",
                database="miniPJ"
            )
            print("Database connected successfully.")
        except mysql.connector.Error as e:
            raise Exception(f"Failed to connect to database: {e}")

    def setup_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="hidecard"
            )
            cursor = conn.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS miniPJ")
            cursor.execute("USE miniPJ")

            # Users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255)
                )
            """)

            # Categories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                )
            """)

            # Items
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    price DECIMAL(10,2),
                    barcode VARCHAR(255),
                    category_id INT,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)

            # Staff
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS staff (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    role VARCHAR(255)
                )
            """)

            # Safe Transactions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safe_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10,2),
                    type VARCHAR(50),
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Add staff_id column + foreign key if not exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA='pos_db'
                AND TABLE_NAME='safe_transactions'
                AND COLUMN_NAME='staff_id'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE safe_transactions 
                    ADD COLUMN staff_id INT,
                    ADD CONSTRAINT fk_safe_staff 
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                """)

            # Sales
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    item_id INT,
                    quantity INT,
                    total DECIMAL(10,2),
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    staff_id INT,
                    FOREIGN KEY (item_id) REFERENCES items(id),
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """)

            # Default admin user
            cursor.execute("""
                INSERT IGNORE INTO users (username, password) 
                VALUES ('admin', 'password')
            """)

            conn.commit()
            conn.close()
            print("Database setup complete.")

        except mysql.connector.Error as e:
            raise Exception(f"Database setup failed: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except mysql.connector.Error as e:
            raise Exception(f"Query execution failed: {e}")

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except mysql.connector.Error as e:
            raise Exception(f"Fetch failed: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

Database().setup_database()
