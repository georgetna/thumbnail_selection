import sqlite3
import hashlib
import random
import string


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(conn, username, email, password):
    c = conn.cursor()
    # Check if the username or email is already registered
    c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    if c.fetchone():
        return False

    hashed_password = hash_password(password)
    c.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hashed_password),
    )
    conn.commit()
    return True


def login_user(conn, username, password):
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    print(users, "users")
    print("PASSWORD", password, username)
    hashed_password = hash_password(password)
    print(hashed_password)
    c.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    )
    return c.fetchone()


def get_user_by_email(conn, email):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    return c.fetchone()


def reset_password(conn, email):
    user = get_user_by_email(conn, email)
    if not user:
        return False

    # Generate a new random password
    new_password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    hashed_password = hash_password(new_password)

    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
    conn.commit()

    # In a real-world application, you would email the new password to the user.
    # For simplicity, we'll just print it here.
    print(f"New password for {email}: {new_password}")
    return True
