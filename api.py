from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/",  methods=['GET'])
def hello_world():
    return {'message': 'your ticks'}

