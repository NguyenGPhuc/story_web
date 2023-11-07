from flask import Flask

app = Flask(name__name__)

@app.route('/')
def hello():
    return "Main page!"