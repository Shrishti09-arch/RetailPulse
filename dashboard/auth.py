import sqlite3
import hashlib
from pathlib import Path
import sqlite3

# Database file
BASE_DIR = Path(__file__).resolve().parent

DB_NAME = BASE_DIR / "users.db"


# =========================
# Create Users Table
# =========================

def create_users_table():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# Password Hashing
# =========================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================
# Register New User
# =========================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:

        c.execute(
            """
            INSERT INTO users
            VALUES (?, ?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================
# Login Existing User
# =========================

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    result = c.fetchone()

    conn.close()

    return result


# =========================
# Check User Exists
# =========================

def user_exists(username):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = c.fetchone()

    conn.close()

    return result is not None


# =========================
# Change Password
# =========================

def update_password(username, new_password):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (
            hash_password(new_password),
            username
        )
    )

    conn.commit()
    conn.close()


# =========================
# Delete User
# =========================

def delete_user(username):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()
    conn.close()