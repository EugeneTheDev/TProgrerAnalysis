import flask
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/quality", methods=["POST"])
def hello_world():
    post = request.json
    return flask.jsonify({
        "response": ""
    })


if __name__ == "__main__":
    app.run()
