# import flask
import re
from flask import Flask

# define instance of app and have flask reference this file with __name__
app = Flask(__name__)


#set up index route with @ and the path
@app.route('/')
#definte the index
def index():
    return "Hello there!"

#if we have errors show them
if __name__ == '__main__':
    app.run(debug=True)