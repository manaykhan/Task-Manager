from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from datetime import datetime
from flask_mail import Mail, Message
from config import mail_username,mail_password

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

db = SQLAlchemy(app)

mail = Mail(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(50), nullable = False)
    task = db.Column(db.String(200), nullable = False)
    date_time = db.Column(db.DateTime, default = datetime.now())

    def __init__(self,userId, task):
        self.userId = userId
        self.task = task
@app.route('/', methods = ['GET','POST'])
def hello_world():
    userId = ''
    if request.method == "POST":
        userId = request.form['userName']
        task = request.form['task']
        todo = Todo(userId = userId,task = task)
        if task != "":
            db.session.add(todo)
            db.session.commit()
    
    allTodo = Todo.query.filter_by(userId=userId).all()
    return render_template("index.html", allTodo=allTodo, userId=userId)

@app.route('/getAll', methods = ['POST']) 
def get_all():
    userId = ''
    if request.method == 'GET':
        userId = request.form['userName']
    allTodo = Todo.query.filter_by(id=userId).all()
    return render_template("index.html", allTodo=allTodo, name=userId)

@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        emailInfo = request.form.get('emailInfo')
        phoneNo = request.form.get('phoneNo')
        message = request.form.get('message')
        msg = Message(subject=f"Mail from {name}",body=f"Name: {name}\nE-Mail: {emailInfo}\nPhone:{phoneNo}\n\n\n{message}", sender = mail_username, recipients=['mahnoor.khan0710@gmail.com'])
        mail.send(msg)
        return render_template("contact.html", success = True)

    return render_template("contact.html")


@app.route('/about', methods = ['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    userId = todo.userId
    db.session.delete(todo)
    db.session.commit()
    allTodos = Todo.query.filter_by(userId=userId).all()
    return render_template("index.html", todos=allTodos)

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    if request.method == 'POST':
        task = request.form['task']
        todo = Todo.query.filter_by(id=id).first()
        todo.task = task
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(id=id).first()
    return render_template("update.html",todo=todo)

if __name__ == "__main__":
    app.run(debug = True)