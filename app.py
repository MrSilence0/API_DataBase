from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conexion a la base de datos
def get_db_connection():
    conn = sqlite3.connect('estudiantes.db')
    conn.row_factory = sqlite3.Row
    return conn


# Crear tabla si no existe
def crear_tabla():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            carrera TEXT NOT NULL,
            semestre INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla()


# ------------------------------
# POST /estudiantes
# Registrar estudiante
# ------------------------------
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():

    datos = request.get_json()

    nombre = datos.get('nombre')
    carrera = datos.get('carrera')
    semestre = datos.get('semestre')

    if not nombre or not carrera or not semestre:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()

    conn.execute(
        'INSERT INTO estudiantes (nombre, carrera, semestre) VALUES (?, ?, ?)',
        (nombre, carrera, semestre)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Estudiante registrado correctamente"}), 201


# ------------------------------
# GET /estudiantes
# Consultar estudiantes
# ------------------------------
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():

    conn = get_db_connection()

    estudiantes = conn.execute(
        'SELECT * FROM estudiantes'
    ).fetchall()

    conn.close()

    lista_estudiantes = []

    for est in estudiantes:
        lista_estudiantes.append({
            "id": est["id"],
            "nombre": est["nombre"],
            "carrera": est["carrera"],
            "semestre": est["semestre"]
        })

    return jsonify(lista_estudiantes)


# ------------------------------
# GET /estudiantes/<id>
# Consultar estudiante por ID
# ------------------------------
@app.route('/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):

    conn = get_db_connection()

    estudiante = conn.execute(
        'SELECT * FROM estudiantes WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if estudiante is None:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    resultado = {
        "id": estudiante["id"],
        "nombre": estudiante["nombre"],
        "carrera": estudiante["carrera"],
        "semestre": estudiante["semestre"]
    }

    return jsonify(resultado)


# Ejecutar API
if __name__ == '__main__':
    app.run(debug=True)