import flask
from flask import Flask
from flask import request

from src import checkquality

app = Flask(__name__)


@app.route("/quality", methods=["POST"])
def hello_world():
    return flask.jsonify(checkquality.perform_full_analysis(request.json))


if __name__ == "__main__":
    app.run()
