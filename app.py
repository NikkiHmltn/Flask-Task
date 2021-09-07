# import flask and render the template folder
from flask import Flask, render_template, url_for

# define instance of app and have flask reference this file with __name__
app = Flask(__name__)


#set up index route with @ and the path
@app.route('/')
#definte the index
def index():
    #renders the index.html template in imported folder
    return render_template('index.html')

#if we have errors show them
if __name__ == '__main__':
    app.run(debug=True)