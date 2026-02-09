from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import secrets
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATABASE = 'users.db'

def init_db():
    """Initialize the database with users table and sample data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            aadhar TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            bank_account TEXT NOT NULL
        )
    ''')

    # Check if table already has data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Insert sample users
        sample_data = [
            ('admin', 'admin123', 'John Doe', 28, '1995-05-15', 'Male',
             '1234-5678-9012', '9876543210', 'john@example.com', '1234567890123456'),
            ('user1', 'pass123', 'Sarah Smith', 32, '1991-08-22', 'Female',
             '9876-5432-1098', '8765432109', 'sarah@example.com', '9876543210987654'),
            ('test', 'test123', 'Mark Johnson', 25, '1998-03-10', 'Male',
             '5555-6666-7777', '7654321098', 'mark@example.com', '5555666677778888'),
        ]

        for data in sample_data:
            cursor.execute('''
                INSERT INTO users
                (username, password, full_name, age, dob, gender, aadhar, phone, email, bank_account)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

    conn.commit()
    conn.close()

def get_user_by_credentials(username, password):
    """
    INTENTIONAL SQL INJECTION VULNERABILITY
    User input is directly concatenated into SQL query without sanitization
    This allows SQL injection attacks like: ' OR '1'='1
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # VULNERABLE: Direct string concatenation - SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        conn.close()
        return None

def get_user(username):
    """
    Get user details by username (this will be used to display on dashboard)
    INTENTIONAL XSS VULNERABILITY: Username is not escaped/sanitized
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Using parameterized query here just to fetch data
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def index():
    """Home page - redirects to login"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - accepts any username and password"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # REMOVED: No validation against database
        # ANY username and password will successfully log in
        if username and password:  # Just check that both fields are not empty
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Please enter username and password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page showing user details"""
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user = get_user(username)

    # If user exists in database, use their details; otherwise generate random details
    if user:
        user_data = {
            'username': username,  # INTENTIONAL XSS: rendered without escaping
            'full_name': user[3],
            'age': user[4],
            'dob': user[5],
            'gender': user[6],
            'aadhar': user[7],
            'phone': user[8],
            'email': user[9],
            'bank_account': user[10]
        }
    else:
        # Generate random user details for any username not in database
        genders = ['Male', 'Female', 'Other']
        user_data = {
            'username': username,  # INTENTIONAL XSS: rendered without escaping
            'full_name': generate_random_name(),
            'age': random.randint(18, 65),
            'dob': generate_random_dob(),
            'gender': random.choice(genders),
            'aadhar': generate_random_aadhar(),
            'phone': generate_random_phone(),
            'email': f"{username}@example.com",
            'bank_account': generate_random_account()
        }

    return render_template('dashboard.html', user=user_data)

def generate_random_name():
    """Generate a random full name"""
    first_names = ['John', 'Sarah', 'Mark', 'Emma', 'Michael', 'Lisa', 'David', 'Jennifer', 'Robert', 'Mary']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_dob():
    """Generate a random date of birth"""
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"

def generate_random_aadhar():
    """Generate a random Aadhar number"""
    return '-'.join([str(random.randint(1000, 9999)) for _ in range(3)])

def generate_random_phone():
    """Generate a random phone number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def generate_random_account():
    """Generate a random bank account number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=5000)
