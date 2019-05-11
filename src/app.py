from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/post", methods=["POST"])
def hello_world():
    data = request.json
    print(data["foo"])
    return "Hello World!"


if __name__ == "__main__":
    app.run()
