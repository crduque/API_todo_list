"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Tasks
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos/user/<user_route>', methods=['GET'])
def handle_hello(user_route):
    username = User.get_user(user_route)
    user_content = username
    return jsonify(user_content), 200

# CREATE USER
@app.route("/todos/user/<user_route>", methods=["POST"])
def create_user(user_route):
    new_user = User(username=user_route)
    new_user.add_user()
    return jsonify(new_user.serialize()), 201

# CREATE TASK
@app.route("/todos/user/<user_route>/list", methods=["POST"])
def create_task(user_route):
    body = request.get_json()
    new_task = Tasks(user_name=user_route, task_text=body["task_text"], task_done=body["task_done"])
    new_task.add_task()
    return jsonify(new_task.serialize())

# READ ALL TASKS
@app.route("/todos/user/<user_route>/list", methods=["GET"])
def read_all_tasks(user_route):
    todo_list = Tasks.get_all_tasks(user_route)
    return jsonify(todo_list)

# UPDATE ONE TASK
@app.route("/todos/user/<user_route>/list", methods=["PUT"])
def update_task(user_route):
    body = request.get_json()
    updated_task = Tasks(user_name=user_route, id=body["id"], task_text=body["task_text"], task_done=body["task_done"])
    updated_task.update_task(user_route, body["id"], body["task_text"], body["task_done"])
    return jsonify(updated_task.serialize())

# # DELETE USER AND ITS TASKS
# @app.route("/todos/user/<user_route>", methods=["DELETE"])
# def delete_user(user_route):
#     pass

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
