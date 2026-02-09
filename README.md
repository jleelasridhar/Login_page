# Vulnerable Web Application - Educational Purpose

This is an intentionally vulnerable web application designed for **educational and security testing purposes only**. It demonstrates common web vulnerabilities: **SQL Injection** and **Cross-Site Scripting (XSS)**.

## Project Structure

```
Vuln_page/
├── app.py                 # Flask backend with vulnerabilities
├── requirements.txt       # Python dependencies
├── users.db              # SQLite database (auto-created on first run)
├── static/
│   └── style.css         # CSS styling
└── templates/
    ├── login.html        # Login page
    └── dashboard.html    # User dashboard after login
```

## Installation & Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default Test Credentials

The database is pre-populated with sample users:

| Username | Password | Full Name |
|----------|----------|-----------|
| admin | admin123 | John Doe |
| user1 | pass123 | Sarah Smith |
| test | test123 | Mark Johnson |

## Features

### Page 1: Login Page
- Modern, attractive UI with gradient background
- Card-style form with proper spacing
- Username and password input fields
- Responsive design for all devices
- Demo credentials displayed

### Page 2: User Dashboard
- Welcome message with username
- Display user details in a card grid layout:
  - Full Name
  - Age
  - Date of Birth
  - Gender
  - Aadhar Number
  - Phone Number
  - Email ID
  - Bank Account Number
- Logout functionality
- Responsive design

## Intentional Vulnerabilities

### 1. SQL Injection Vulnerability

**Location:** `app.py` - `get_user_by_credentials()` function

**Issue:** User input is directly concatenated into SQL queries without sanitization.

**How to Test:**
- Go to login page
- Username: `admin' OR '1'='1`
- Password: (any value)
- Click Login - This will bypass the password check!

**Why it works:** The query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'
```

This is always true because `'1'='1'` is always true.

### 2. Cross-Site Scripting (XSS) Vulnerability

**Location:** `templates/dashboard.html` - Welcome section

**Issue:** Username is rendered directly in HTML without escaping or sanitization.

**How to Test:**
- Go to login page
- Username: `<script>alert('XSS Vulnerability!')</script>`
- Password: `<script>alert('XSS Vulnerability!')</script>`
- Click Login
- In the browser console, inject this as a user first, then observe XSS execution

**Alternative approach (requires database modification):**
You can directly insert a malicious username into the database:
```python
INSERT INTO users (username, password, full_name, age, dob, gender, aadhar, phone, email, bank_account)
VALUES ('<img src=x onerror="alert(\"XSS\")">', 'pass', 'Test User', 25, '2000-01-01', 'Male', '1111-2222-3333', '1234567890', 'test@example.com', '1111111111111111');
```

## File Details

### app.py
- **Database:** SQLite (users.db)
- **Routes:**
  - `/` - Home (redirects to login)
  - `/login` - Login page (GET/POST)
  - `/dashboard` - User dashboard (requires authentication)
  - `/logout` - Logout and clear session

### templates/login.html
- Modern login form with gradient styling
- Automatic redirect to dashboard on successful login
- Demo credentials section
- Error message display

### templates/dashboard.html
- Welcome message with injected username (XSS vulnerability)
- User details displayed in responsive grid
- Logout button and action buttons

### static/style.css
- Gradient background (purple to pink)
- Card-based UI design
- Hover effects and animations
- Fully responsive design (mobile, tablet, desktop)

## Important Security Notes

⚠️ **This application is INTENTIONALLY VULNERABLE for educational purposes.**

### DO NOT:
- Deploy this in production
- Use this code as a reference for secure applications
- Store sensitive data in this application
- Use this on public internet without proper firewall

### TO USE SAFELY:
- Run only on localhost (http://localhost:5000)
- Use in isolated lab environments
- Use for learning and security training only
- Delete after learning

## Usage Instructions

### Normal Login (If Testing without SQL Injection):
1. Go to http://localhost:5000
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click Login
5. View dashboard with user details
6. Click Logout to return to login

### Testing SQL Injection:
1. Go to http://localhost:5000
2. Enter username: `admin' OR '1'='1` (with quotes and backtick)
3. Enter password: (anything, e.g., "test")
4. Click Login - Password check is bypassed!
5. Observe you're logged in without correct password

### Testing XSS:
1. Go to database and insert user with XSS payload
2. Or modify the HTML in browser dev tools to test
3. Script tags should execute
4. Can test with event handlers: `<img src=x onerror=alert('XSS')>`

## Database Schema

```sql
CREATE TABLE users (
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
```

## Educational Value

This application helps you understand:
1. **SQL Injection:** How parameterized queries protect against injection attacks
2. **XSS (Cross-Site Scripting):** Why user input must be escaped/sanitized
3. **Web Security:** Basic concepts of secure web development
4. **Flask Framework:** Basic Flask application structure
5. **Session Management:** Using Flask sessions for authentication

## Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Cross-Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [Flask Security](https://flask.palletsprojects.com/)

## License

Educational Only - Not for Production Use

## Disclaimer

This application is provided solely for educational and authorized security testing purposes. The author is not responsible for misuse or any damage caused by this software.
