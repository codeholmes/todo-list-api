from app import TodoListAPI
from flask import Flask

app = Flask(__name__)
api = TodoListAPI()


@app.route("/", methods=["POST", "GET"])
def index():
    return api.index()


@app.route("/create", methods=["POST"])
def create():
    return api.create()


@app.route("/delete", methods=["DELETE"])
def delete():
    return api.delete()


@app.route("/update_task", methods=["POST"])
def update_task():
    return api.update_task()


@app.route("/update_status", methods=["POST"])
def update_status():
    return api.update_status()


app.run(debug=True)
