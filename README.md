# PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos

Materia: Programación sobre Redes · 2° cuatrimestre 2026 · Práctica Formativa Obligatoria 2 (semana 8)

## Descripción

API REST en Python (Flask) con autenticación básica y persistencia en SQLite:

- `POST /registro`: registra usuarios con contraseña **hasheada** (nunca en texto plano).
- `POST /login`: verifica credenciales y permite el acceso.
- `GET /tareas`: devuelve un HTML de bienvenida (acceso a la gestión de tareas).

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `servidor.py` | API Flask + SQLite + hasheo de contraseñas (Werkzeug) |
| `cliente.py` | Cliente en consola que interactúa con la API |
| `tareas.db` | Base de datos SQLite generada al primer arranque |

## Requisitos

- Python 3
- Flask (`pip install flask`)
- Requests (`pip install requests`)

## Cómo ejecutar

### 1. Iniciar el servidor

```bash
python3 servidor.py
```

El servidor escucha en `http://127.0.0.1:5000`. Al arrancar crea la base `tareas.db` (tablas `usuarios` y `tareas`).

### 2. Probar con el cliente de consola

```bash
python3 cliente.py
```

Opciones: 1. Registrarse · 2. Iniciar sesión · 3. Ver tareas (HTML) · 4. Salir.

### 3. Probar con curl

```bash
# Registro
curl -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario":"leo","contraseña":"1234"}'

# Inicio de sesión
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"leo","contraseña":"1234"}'

# Acceso a tareas (HTML de bienvenida)
curl http://127.0.0.1:5000/tareas
```

## Pruebas realizadas (04/10/2026)

| Caso | Comando | Resultado |
|------|---------|-----------|
| Registro OK | `POST /registro {"usuario":"leo","contraseña":"1234"}` | `{"mensaje":"Usuario registrado correctamente."}` (HTTP 201) |
| Registro duplicado | `POST /registro` mismo usuario | `{"error":"El usuario ya existe."}` (HTTP 409) |
| Registro sin datos | `POST /registro {"usuario":"x"}` | `{"error":"Usuario y contraseña son obligatorios."}` (HTTP 400) |
| Login OK | `POST /login` credenciales válidas | `{"mensaje":"Inicio de sesion exitoso..."}` (HTTP 200) |
| Login inválido | `POST /login` contraseña incorrecta | `{"error":"Credenciales invalidas."}` (HTTP 401) |
| Tareas | `GET /tareas` | HTML de bienvenida (HTTP 200) |

Verificación de la base: la columna `contrasena_hash` contiene un hash **scrypt** (nunca la contraseña en texto plano).

## Respuestas conceptuales

### ¿Por qué hashear contraseñas?

- **Nunca se almacenan en texto plano**: si la base de datos es comprometida, un atacante no obtiene las contraseñas reales, sino su hash.
- **Protección ante filtraciones y reutilización**: los usuarios suelen reutilizar la misma contraseña en varios servicios; exponer el texto plano los expondría en todos lados.
- **Hasheo con sal (salt)**: Werkzeug genera un hash con una sal aleatoria por usuario (scrypt), por lo que dos usuarios con la misma contraseña tendrán hashes distintos y cada hash es costoso de revertir.
- **Clave única e irreversible**: el hash no se "desencripta"; al iniciar sesión se vuelve a hashear lo ingresado y se compara (`check_password_hash`).

### ¿Ventajas de usar SQLite en este proyecto?

- **Sin servidor de base de datos**: SQLite es una base embebida (un archivo `.db`); no hace falta instalar/configurar un motor como MySQL o PostgreSQL.
- **Simple y liviana**: ideal para aplicaciones de este tamaño y para la persistencia entre reinicios del servidor.
- **Estándar de Python**: el módulo `sqlite3` viene incluido en la biblioteca estándar, sin dependencias extra.
- **Confiabilidad y portabilidad**: transacciones ACID, y el archivo se puede copiar/mover con facilidad.
- **Suficiente para el proyecto**: el volumen de datos de una gestión de tareas no demanda una base cliente-servidor.

## Notas

- Repositorio: https://github.com/hleopary/pfo2-api-tareas (rama de trabajo + GitHub Pages con el README).
- Se usa `werkzeug.security` (`generate_password_hash` / `check_password_hash`), la librería recomendada con Flask.
- Puerto por defecto: 5000 (configurable en `servidor.py`).