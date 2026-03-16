from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Conexión a la base de datos
conexion = psycopg2.connect(
    host="dpg-d6rkug450q8c73f4i78g-a.oregon-postgres.render.com",
    database="biblioteca_db_2sq1",
    user="biblioteca_db_2sq1_user",
    password="BnEOA2fWt3Khmaoulk6EE3LQfMb5ptwL",
    port="5432"
)

cursor = conexion.cursor()


# LOGIN
@app.route('/')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def validar_login():

    usuario = request.form['usuario']
    password = request.form['password']

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s AND password=%s",
        (usuario, password)
    )

    user = cursor.fetchone()

    if user:
        return redirect('/menu')
    else:
        return render_template("login.html", error="Usuario o contraseña incorrectos")


# MENU
@app.route('/menu')
def menu():
    return render_template("menu.html")


# LISTAR LIBROS
@app.route('/libros')
def libros():

    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()

    return render_template("libros.html", libros=libros)


# FORMULARIO AGREGAR
@app.route('/agregar')
def agregar():
    return render_template("agregar.html")


# GUARDAR LIBRO
@app.route('/guardar', methods=['POST'])
def guardar():

    titulo = request.form['titulo']
    autor = request.form['autor']
    anio = int(request.form['anio'])
    precio = float(request.form['precio'])

    # Validaciones
    if anio < 1000 or anio > 2100:
        return "Error: Año inválido"

    if precio < 0 or precio > 1000000:
        return "Error: Precio inválido"

    try:
        cursor.execute(
            "INSERT INTO libros (titulo, autor, anio, precio) VALUES (%s,%s,%s,%s)",
            (titulo, autor, anio, precio)
        )

        conexion.commit()

    except:
        conexion.rollback()
        return "Error al guardar el libro"

    return redirect('/libros')


# ELIMINAR LIBRO
@app.route('/eliminar/<int:id>')
def eliminar(id):

    try:
        cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
        conexion.commit()

    except:
        conexion.rollback()
        return "Error al eliminar"

    return redirect('/libros')


# EDITAR LIBRO
@app.route('/editar/<int:id>')
def editar(id):

    cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
    libro = cursor.fetchone()

    return render_template("editar.html", libro=libro)


# ACTUALIZAR LIBRO
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):

    titulo = request.form['titulo']
    autor = request.form['autor']
    anio = int(request.form['anio'])
    precio = float(request.form['precio'])

    # Validaciones
    if anio < 1000 or anio > 2100:
        return "Error: Año inválido"

    if precio < 0 or precio > 1000000:
        return "Error: Precio inválido"

    try:
        cursor.execute(
            "UPDATE libros SET titulo=%s, autor=%s, anio=%s, precio=%s WHERE id=%s",
            (titulo, autor, anio, precio, id)
        )

        conexion.commit()

    except:
        conexion.rollback()
        return "Error al actualizar el libro"

    return redirect('/libros')


# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/')


# EJECUCIÓN LOCAL
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)