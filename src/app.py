import flask
from flask import Flask
from flask import request

from src import checkquality
from src import predict

app = Flask(__name__)


@app.route("/quality", methods=["POST"])
def quality_post():
    return flask.jsonify(checkquality.perform_full_analysis(request.json))


@app.route("/prediction", methods=["POST"])
def predictions_post():
    return flask.jsonify(predict.perform_full_prediction(request.json))


if __name__ == "__main__":
    app.run()
