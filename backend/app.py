from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect, generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import os
import secrets

app = Flask(__name__)

# Secret key used by Flask to sign session cookies. Flask uses this
# to cryptographically sign the session cookie that references
# server-side session data. Keep this secret in production.
app.secret_key = secrets.token_hex(32)

# app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# tuotannossa:
# app.config["SESSION_COOKIE_SECURE"] = True

CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {
        "origins": "http://127.0.0.1:5173",
        "allow_headers": ["Content-Type", "X-CSRFToken"],
        "methods": ["GET", "POST", "OPTIONS"]
    }}
)

csrf = CSRFProtect(app)

DATABASE = "users.db"

def create_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
create_db()

@app.route("/rekisteröidy", methods=["POST"])
@csrf.exempt
def rekisteroidy():

    # Endpoint: POST /rekisteröidy
    # - Expects JSON: { name, password }
    # - Validates input, hashes the password with Werkzeug and stores
    #   a new user row in the SQLite `users` table.

    data = request.get_json()

    username = data.get("name")
    password = data.get("password")
    print(f"Rekisteröitymisyritys: {username}")
    
    if not username or not password:
        return jsonify({
            "error": "Puuttuvat tiedot"
        }), 400

    if len(username) > 50:
        return jsonify({
            "error": "Liian pitkä käyttäjänimi"
        }), 400

    password_hash = generate_password_hash(password)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT id FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({
            "error": "Käyttäjä on jo olemassa"
        }), 409

    cursor.execute(
        """
        INSERT INTO users(username,password_hash)
        VALUES (?,?)
        """,
        (username, password_hash)
    )

    conn.commit()
    conn.close()
    print(f"Rekisteröity uusi käyttäjä: {username}")
    return jsonify({
        "message": "Rekisteröinti onnistui"
    }), 201

@app.route("/kirjaudu", methods=["POST"])
@csrf.exempt
def kirjaudu():

    data = request.get_json()

    username = data.get("name")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Puuttuvat tiedot"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    user = cursor.execute(
        """
        SELECT id,password_hash
        FROM users
        WHERE username=?
        """,
        (username,)
    ).fetchone()

    conn.close()

    if not user:
        return jsonify({
            "error": "Virheellinen tunnus tai salasana"
        }), 401

    user_id = user[0]
    stored_hash = user[1]

    if not check_password_hash(stored_hash, password):
        return jsonify({
            "error": "Virheellinen tunnus tai salasana"
        }), 401

    session["user_id"] = user_id

    return jsonify({
        "message": "Kirjautuminen onnistui"
    }), 200


@app.route("/me", methods=["GET"])
def me():
    # Endpoint: GET /me
    # - Used by the frontend to verify whether the current browser
    #   session is authenticated. The browser must send the session
    #   cookie; this is handled automatically when `axios` is used
    #   with `withCredentials: true` on the client.
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"authenticated": False}), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    user = cursor.execute(
        "SELECT username FROM users WHERE id=?",
        (user_id,)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"authenticated": False}), 401

    return jsonify({"authenticated": True, "username": user[0]}), 200


@app.route("/logout", methods=["POST"])
@csrf.exempt
def logout():
    # Endpoint: POST /logout
    # - Clears the `user_id` from the session so subsequent `/me`
    #   checks return unauthenticated.
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200


if __name__ == "__main__":
    app.run(debug=True)