from flask import Flask, request, make_response, render_template, url_for, redirect
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__, template_folder="templates")


def db_connection():
    connection = sqlite3.connect('database')
    connection.row_factory = sqlite3.Row
    return connection


def get_id_product(pid):
    connection = db_connection()
    prod = connection.execute('SELECT * FROM products WHERE id = ?',
                        (pid,)).fetchone()
    connection.close()
    if prod is None:
        abort(404)
    return prod


@app.route("/")
@app.route("/products")
def products_list():
    connection = db_connection()
    products = connection.execute('SELECT * FROM products').fetchall()
    connection.close()
    return render_template("products/list.html", products=products)


@app.route("/products/<int:pid>/delete", methods=('GET', 'POST'))
def product_delete(pid):
    connection = db_connection()
    prod = get_id_product(pid)
    if request.method == 'GET':
        return render_template('products/delete.html', product=prod)
    if request.method == 'POST':
        connection.execute("DELETE FROM products WHERE id=?", (prod['id'],))
        connection.commit()
        connection.close()
        return redirect(url_for('products_list'))


@app.route('/products/<int:pid>/edit', methods=('GET', 'POST'))
def product_edit(pid):
    prod = get_id_product(pid)
    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        if not name:
            print('Кто такой сулат бабирзянов?')
        else:

            connection = db_connection()
            connection.execute('UPDATE products SET name = ?, price = ?, description = ?'
                         ' WHERE id = ?',
                         (name, price, description, prod['id']))
            connection.commit()
            connection.close()
            return redirect(url_for('products_list'))

    return render_template('products/edit.html', product=prod)


@app.route('/products/create', methods=('GET', 'POST'))
def product_create():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        if not name:
            print('веб это не мое')
        else:
            connection = db_connection()
            connection.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                         (name, price, description))
            connection.commit()
            connection.close()
            return redirect(url_for('products_list'))

    return render_template('products/create.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5010, debug=True)
