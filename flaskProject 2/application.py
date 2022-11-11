from flask import Flask, request, make_response, render_template, url_for, redirect
from faker import Faker
import random

app = Flask(__name__, template_folder="templates")

fake = Faker("ru_RU")

class Product:
	def __init__(self, pid):
		self.pid = pid
		self.name = fake.name()
		self.description = fake.text()
		self.color = fake.color()
		self.price = random.random() * 100

database = [Product(pid) for pid in range(20)]

@app.route("/products")
def products_list():
	content = render_template("products/list.html", products=database)
	res = make_response(content)

	if "background-color" not in request.cookies:
		res.set_cookie("background-color", "1", max_age=10)
		print('Кука установлена!')
	else:
		counter = int(request.cookies.get('background-color'))
		counter += 1
		res.set_cookie("background-color", str(counter), max_age=10)

		# how to del cookie
		#res.delete_cookie("counter")

		print(f"зашёл {counter} раз")

	return res

@app.route("/products/<int:pid>")
def product_details(pid):
	pid = int(pid)
	if pid < len(database):
		product = database[pid]
		return render_template("products/detail.html", product=product)
	return "lol not found", 404

@app.route("/products/delete/<int:pid>")
def product_delete(pid):
	pid = int(pid)
	if pid < len(database):
		product = database[pid]
		return render_template("products/delete.html", product=product)
	return "lol not found", 404


@app.route("/products/update/<int:pid>")
def product_update(pid):
	pid = int(pid)
	# /////
	# valid forms
	if pid < len(database):
		product = database[pid]
		return render_template("products/update.html", product=product)
	return "lol not found", 404

def int_validator(value):
	if value and all(map(str.isdigit, value)):
		return int(value)
	return None

def form_valid(form):
	"""
	Function for form validation
	Args:
		form (dict):
	Returns:
		bool: True if all is ok
	"""
	return all(map(len, form.values()))

@app.route("/products/create", methods=['GET', 'POST'])
def product_create():
	if request.method == "POST":
		if form_valid(request.form):
			name = request.form.get("name")
			price = int_validator(request.form.get("price"))
			color = request.form.get("color")
			description = request.form.get("description")

			product = Product(len(database))
			product.name = name
			product.price = price
			product.color = color
			product.description = description

			database.append(product)

			return redirect(url_for('index'))

	return render_template("products/create.html")

@app.route("/")
@app.route("/home")
def index():
	return redirect("/products")



if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5005, debug=True)