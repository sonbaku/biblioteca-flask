from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# 🔥 CONEXIÓN CORREGIDA (OPCIÓN A)
conexion = psycopg2.connect(
    host="dpg-d7ipq54vikkc73enaad0-a.oregon-postgres.render.com",
    database="biblioteca_db2",
    user="biblioteca_db2_user",
    password="ZL1gCzsnurlVvdROL4ZcdLkOoMtIjzLS",
    port="5432",
    sslmode="require"
)

cursor = conexion.cursor()


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


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/libros')
def libros():

    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()

    return render_template("libros.html", libros=libros)


@app.route('/agregar')
def agregar():
    return render_template("agregar.html")


@app.route('/guardar', methods=['POST'])
def guardar():

    titulo = request.form['titulo']
    autor = request.form['autor']
    anio = request.form['anio']
    precio = request.form['precio']

    cursor.execute(
        "INSERT INTO libros (titulo, autor, anio, precio) VALUES (%s,%s,%s,%s)",
        (titulo, autor, anio, precio)
    )

    conexion.commit()

    return redirect('/libros')


@app.route('/eliminar/<int:id>')
def eliminar(id):

    cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
    conexion.commit()

    return redirect('/libros')


@app.route('/editar/<int:id>')
def editar(id):

    cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
    libro = cursor.fetchone()

    return render_template("editar.html", libro=libro)


@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):

    titulo = request.form['titulo']
    autor = request.form['autor']
    anio = request.form['anio']
    precio = request.form['precio']

    cursor.execute(
        "UPDATE libros SET titulo=%s, autor=%s, anio=%s, precio=%s WHERE id=%s",
        (titulo, autor, anio, precio, id)
    )

    conexion.commit()

    return redirect('/libros')


@app.route('/logout')
def logout():
    return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)