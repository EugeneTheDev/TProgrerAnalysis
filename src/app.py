import flask
from flask import Flask
from flask import request

from src import analyse
from src import checkquality
from src import rss

app = Flask(__name__)


@app.route("/quality", methods=["POST"])
def quality_post():
    return flask.jsonify(checkquality.perform_full_analysis(request.json))


@app.route("/analyse", methods=["POST"])
def predictions_post():
    return flask.jsonify(analyse.perform_full_prediction(request.json))


@app.route("/rss", methods=["GET"])
def get_rss():
    return flask.jsonify(rss.read_news())


if __name__ == "__main__":
    app.run()
