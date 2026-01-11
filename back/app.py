from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Создание БД
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

init_db()

# Регистрация
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = generate_password_hash(data["password"])

    try:
        with sqlite3.connect("users.db") as conn:
            conn.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )
        return jsonify({"message": "Пользователь зарегистрирован"})
    except:
        return jsonify({"message": "Email уже существует"}), 400


# Логин
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    with sqlite3.connect("users.db") as conn:
        user = conn.execute(
            "SELECT password FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Успешный вход"})
    else:
        return jsonify({"message": "Неверный email или пароль"}), 401


if __name__ == "__main__":
    app.run(debug=True)
