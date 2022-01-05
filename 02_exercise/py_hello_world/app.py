from flask import Flask

app = Flask(__name__)

my_name = "Natalia"


@app.route("/")
def greetings():
    return f"Hello, World {my_name}"


@app.route("/who")
def who():
    return my_name


if __name__ == "__main__":
    app.run()
