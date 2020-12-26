from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Adding failed!'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<taskid>')
def delete_task(taskid):
    try:
        Todo.query.filter_by(id=taskid).delete()
        db.session.commit()
        return redirect('/')
    except:
        return "Delete failed!"

@app.route('/update/<taskid>',methods=['POST','GET'])
def update_task(taskid):
    if request.method == 'POST':
        try:
            current_task = Todo.query.filter_by(id=taskid).first()
            current_task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return "Update failed!"
    else:
        current_task = Todo.query.filter_by(id=taskid).first()
        print(current_task.id)
        return render_template('update.html',task = current_task)

if __name__ == "__main__":
    app.run(debug=True)