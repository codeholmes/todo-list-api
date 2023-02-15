from app import TodoListAPI
from flask import Flask

app = Flask(__name__)
api = TodoListAPI()


@app.route("/todo", methods=["GET"])
def todo():
    """Only GET method allowed"""
    return api.todo()


@app.route("/create", methods=["POST"])
def create():
    """Only POST method allowed"""
    return api.create()


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    """Only DELETE method allowed"""
    return api.delete(id)


@app.route("/update_task/<int:id>", methods=["PUT"])
def update_task(id):
    """Only PUT method allowed"""
    return api.update_task(id)


@app.route("/update_status/<int:id>", methods=["PUT"])
def update_status(id):
    """Only PUT method allowed"""
    return api.update_status(id)


app.run(debug=True)
