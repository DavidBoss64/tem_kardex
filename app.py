from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

def init_database():
    conn = sqlite3.connect('kardex.db')

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS personas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_database()

#LISTADO DE REGISTROS
@app.route('/')
def index():
    conn = sqlite3.connect('kardex.db')
    #PERMITE MANEJAR EL R3GISTRO COMO UN DIICCIONARIO
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    conn.close()

    return render_template("index.html", personas = personas)

#AGREGAR REGISTRO
@app.route('/create')
def create():
    return render_template('create.html')

#GUARDAR REGISTRO NUEVO
@app.route('/save', methods = ['POST'])
def save():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']

    conn = sqlite3.connect('kardex.db')
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO personas (nombre, telefono, fecha_nac)
                    VALUES(?,?,?)""",(nombre,telefono,fecha_nac))
    conn.commit()
    conn.close()
    return redirect('/')

#EDITAR REEGISTRO
@app.route('/edit/<int:id>')
def persona_edit(id):
    conn = sqlite3.connect('kardex.db')
    conn.row_factory =sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("edit.html",persona = persona)

#GUARDAR ACTUALIZACION DE REGISTRO
@app.route('/update',methods = ['POST'])
def update():
    id =request.form['id']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']

    conn = sqlite3.connect('kardex.db')
    cursor=conn.cursor()

    cursor.execute(""" 
    UPDATE personas SET nombre=?, telefono=?, fecha_nac=? WHERE id=?
    """,(nombre, telefono, fecha_nac, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def personas_delete(id):
    conn =sqlite3.connect('kardex.db')
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM personas WHERE id = ?""", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)