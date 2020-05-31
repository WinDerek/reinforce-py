from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello from Flask backend!"
