from flask import Flask, render_template
from flask_cors import CORS
from flask import request
from flask import jsonify
from backend.reinforce import evaluate_policy_by_one_sweep, improve_policy

app = Flask(__name__)
CORS(app)

@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello from Flask backend!"


@app.route("/api/dynamic_programming/policy_evaluation", methods=['GET', 'POST'])
def policy_evaluation():
    grid_data_list = request.json

    for grid_data in grid_data_list:
        print(grid_data)

    return jsonify(evaluate_policy_by_one_sweep(grid_data_list))


@app.route("/api/dynamic_programming/policy_improvement", methods=['GET', 'POST'])
def policy_improvement():
    grid_data_list = request.json

    for grid_data in grid_data_list:
        print(grid_data)

    return jsonify(improve_policy(grid_data_list))
