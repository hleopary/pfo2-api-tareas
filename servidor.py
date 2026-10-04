import os
import sqlite3

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tareas.db")

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contrasena_hash TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        """
    )
    conn.commit()
    conn.close()


def usuario_por_nombre(nombre):
    conn = get_db()
    fila = conn.execute("SELECT * FROM usuarios WHERE usuario = ?", (nombre,)).fetchone()
    conn.close()
    return fila


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son obligatorios."}), 400

    if usuario_por_nombre(usuario):
        return jsonify({"error": "El usuario ya existe."}), 409

    contrasena_hash = generate_password_hash(contrasena)

    conn = get_db()
    conn.execute(
        "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
        (usuario, contrasena_hash),
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado correctamente."}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son obligatorios."}), 400

    fila = usuario_por_nombre(usuario)
    if fila is None or not check_password_hash(fila["contrasena_hash"], contrasena):
        return jsonify({"error": "Credenciales invalidas."}), 401

    return jsonify({"mensaje": "Inicio de sesion exitoso. Acceso a tareas permitido."}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>PFO 2 - Gestión de Tareas</title>
    </head>
    <body>
      <h1>Bienvenido a la API de Gestión de Tareas</h1>
      <p>API REST de la PFO 2 (Programación sobre Redes).</p>
      <p>Endpoints disponibles: POST /registro, POST /login, GET /tareas.</p>
    </body>
    </html>
    """
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    init_db()
    if not os.path.exists(DB_PATH):
        print("Base de datos creada.")
    app.run(debug=False, host="127.0.0.1", port=5000)