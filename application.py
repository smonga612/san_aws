from flask import Flask
application = Flask(__name__)

@application.route("/")
def index():
    return "<h1>My application is work fine<h1>"

@application.route("/hello")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    application.run(port=5000, debug=True)