from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

SECRET_KEY = "super-secret-key"

# ---------- БД ----------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

init_db()

# ---------- РЕГИСТРАЦИЯ ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Заполните все поля"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )
        return jsonify({"message": "Регистрация успешна"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Пользователь уже существует"}), 400

# ---------- ЛОГИН ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    with get_db() as db:
        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Неверный email или пароль"}), 401

    token = jwt.encode({
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})

# ---------- ПРОФИЛЬ (JWT) ----------
@app.route("/profile", methods=["GET"])
def profile():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"message": "Нет токена"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"message": "Неверный или просроченный токен"}), 401

    return jsonify({
        "email": payload["email"]
    })



@app.route("/users", methods=["GET"])
def get_users():
    with get_db() as db:
        users = db.execute("SELECT id, email FROM users").fetchall()

    return jsonify([
        {"id": u["id"], "email": u["email"]}
        for u in users
    ])


if __name__ == "__main__":
    app.run(debug=True)