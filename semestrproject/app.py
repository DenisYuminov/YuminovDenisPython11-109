import sqlite3
import requests
from flask import render_template, session
from flask_session import Session
from flask_bcrypt import Bcrypt
import os
import vk_api
from flask import Flask, flash, request, redirect, url_for
from scripts.vk import main, auth_handler
bcrypt = Bcrypt()
app = Flask(__name__, template_folder="templates")

app.config['UPLOAD_FOLDER'] = "static/uploads"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'e[rl349534hetdgrig4uwot5a3whef;eqt;wy3yg'
#
Session(app)
k_auth = 'auth'


def get_my_id():
    conn = get_db_connection()
    login = session['username']
    user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
    conn.close()
    return user['id']


def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post_id(pid):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (pid,)).fetchone()
    conn.close()
    if post is None:
        return 0
    return post


def is_login():
    return session.get('auth')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = None
    return redirect("/")


@app.route("/")
@app.route("/posts", methods=('GET', 'POST'))
def products_list():
    con = get_db_connection()
    posts = con.execute('SELECT * FROM posts').fetchall()
    con.close()
    return render_template("main.html", products=posts)


@app.route("/posts/<int:pid>/delete", methods=('GET', 'POST'))
def product_delete(pid):
    conn = get_db_connection()
    product = get_post_id(pid)
    if request.method == 'GET':
        return render_template('delete.html', product=product)
    if request.method == 'POST':
        conn.execute("DELETE FROM posts WHERE id=?", (product['id'],))
        conn.commit()
        conn.close()
        return redirect(url_for('products_list'))


@app.route('/myprofile', methods=('GET','POST'))
def get_profile_info():
    con = get_db_connection()
    user_id = get_my_id()
    posts = con.execute('SELECT * FROM posts WHERE user_id=?', (user_id,)).fetchall()
    size = len(posts)
    return render_template('profile.html', products=posts, size=size)

@app.route('/<int:pid>/edit', methods=('GET', 'POST'))
def product_edit(pid):
    product = get_post_id(pid)
    if request.method == 'POST':

        text = request.form['text']
        user_id = get_my_id()
        session['user_id'] = user_id
        if not text:
            print('Введите имя вашей любимой учительницы...')
        else:
            if user_id == product['user_id']:
                conn = get_db_connection()
                conn.execute('UPDATE posts SET text = ?'
                             ' WHERE id = ?',
                             (text, product['id']))
                conn.commit()
                conn.close()
                return redirect(url_for('products_list'))

    return render_template('update.html', product=product)


@app.route('/create', methods=('GET', 'POST'))
def product_create():
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            print('Введите имя вашей любимой учительницы...')
        else:
            conn = get_db_connection()
            login = session['username']
            if login:
                user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
                insert(table_name='posts', text=text, user_id=user['id'])
                conn.commit()
                conn.close()
                return redirect(url_for('products_list'))
    return render_template('create.html')



@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')

        conn = get_db_connection()

        user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['vk_auth'] = False
            session['username'] = request.form.get('login')
            return redirect(url_for('products_list'))

    return render_template('login.html')


def insert(table_name, **kwargs):
    conn = get_db_connection()
    arg_q = ', '.join(["?"] * (len(kwargs)))
    arg_names = ",".join(kwargs.keys())

    arg_values = tuple(kwargs.values())
    sql_raw = f"insert into {table_name} ({arg_names}) values ({arg_q})"
    conn.execute(sql_raw, arg_values)
    conn.commit()
    conn.close()


@app.route("/signup", methods=['GET', "POST"])
def signup():
    if request.method == "POST":
        login = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchall()

        if not user and password1 == password2 and len(password1) != 0:
            pw_hash = bcrypt.generate_password_hash(password1)
            insert(table_name='users', login=login, password=pw_hash)

            session['login_name'] = request.form.get('login')
            session[k_auth] = True
            session['vk_auth'] = False

            return redirect(url_for('login'))

    return render_template('signup.html')




@app.route("/login/vk_auth", methods=['GET', "POST"])
def vk_login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        # key = request.form.get('key')
        conn = get_db_connection()

        username = main(login, password)

        user = conn.execute("SELECT * FROM users WHERE login = ?", (username,)).fetchone()
        if not user and len(password) != 0:
            pw_hash = bcrypt.generate_password_hash(password)
            insert(table_name='users', login=username, password=pw_hash)
            conn.commit()
            conn.close()

        session['vk_auth'] = True
        session['username'] = username
        return redirect(url_for('products_list'))
    return render_template('vk_auth.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
