from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    db='contactos'
)
cursor = con.cursor()

app = Flask(__name__)
app.secret_key = 'mi_llave'


@app.route('/')
def Index():
    sql = """SELECT * FROM contactos"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    return render_template('index.html', contactos=datos)


@app.route('/add', methods=['POST'])
def add_contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        sql = """INSERT INTO contactos (nombre, apellido, telefono, email) VALUES(%s, %s, %s, %s)"""
        valores = (nombre, apellido, telefono, email)
        cursor.execute(sql, valores)
        con.commit()
        flash('Contacto agregado con exito')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contacto(id):
    cursor.execute("""DELETE FROM contactos where id = {0}""".format(id))
    con.commit()
    flash('Contacto eliminado con exito')
    return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    sql = "SELECT * FROM contactos WHERE id = %s"
    cursor.execute(sql, (id, ))
    data = cursor.fetchall()

    return render_template('edit-contact.html', contacto=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contacto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        sql = """update contactos
        set nombre = %s,
        apellido = %s,
        telefono = %s,
        email = %s
        where id = %s"""
        cursor.execute(sql, (nombre, apellido, telefono, email, id, ))
        con.commit()
        flash('Contacto actualizado con exito')
        return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
