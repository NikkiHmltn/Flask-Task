# import flask and render the template folder
import re
from flask import Flask, render_template, url_for, request, redirect
#import sql-alchemy
from flask_sqlalchemy import SQLAlchemy
#sqllite doesnt have builtin date, time, or datetime so import it from sqlalchemy
from datetime import datetime

# define instance of app and have flask reference this file with __name__
app = Flask(__name__)
#config the database. 3 /'s are used for a relative location, not direct path followed by name of db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#init database
db = SQLAlchemy(app)

#creation of the Todo model
class Todo(db.Model):
    #make an ID column that is an integer and the primary key
    id = db.Column(db.Integer, primary_key=True)
    #content is for user content that we dont want them to create while it's empty, and give it a character limit of 200 characters
    content = db.Column(db.String(200), nullable=False)
    #date is used for timestamping like any other db, but set default to imported datetime
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #enriches classes and returns a string as the representation of the object
    def __repr__(self):
        return '<Task %r' % self.id


#set up index route with @ and the path
#methods of post and get allow us to not only get info but post it too
@app.route('/', methods=['POST', 'GET'])
#definte the index
def index():
    if request.method == 'POST':
        #the form comes from the form inside of the html and passes the content in
        task_content = request.form['content']
        #creates a todo with the form content
        new_task = Todo(content=task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue adding your task'

    else: 
        # looks at all data in creation order and returns all of them in order
        tasks = Todo.query.order_by(Todo.date_created).all()
    #renders the index.html template in imported folder
        return render_template('index.html', tasks=tasks)

#set up delete route with brackets and specify the unique data and its type. this case is unique integer called id
@app.route("/delete/<int:id>")
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except: 
        return 'There was a problem deleting the task'

#set up update route
@app.route("/update/<int:id>", methods=["POST", 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST': 
        #set current task content to form content box
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect('/')
        except: 
            return "There was an issue updating your task"
    else: 
        return render_template('update.html', task=task)

#if we have errors show them
if __name__ == '__main__':
    app.run(debug=True)