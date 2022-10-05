from flask import Flask, render_template, url_for

app = Flask(__name__)

counter = 0

@app.route("/")
@app.route("/products")
def hello():
    return render_template("products.html")

@app.route("/test")
def zero():
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=10009, debug=True)