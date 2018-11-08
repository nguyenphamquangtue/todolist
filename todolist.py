from flask import Flask, jsonify, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rockship:@localhost:5433/todolist'

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.BIGINT, primary_key=True)
    content = db.Column(db.JSON)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, data):
        self.content = data
        self.done = False
    
    def __repr__(self):
        return '<Content %s>' % self.content

@app.route('/')
def get_all_list():
    list_of_todo = Todo.query.all()
    print(list_of_todo)
    return jsonify(list_of_todo, None)


@app.route('/task', methods=['POST'])
def add_to_do():
    data = request.get_json()

    if not data:
        return abort(400)
    
    task = Todo(data)
    print(task)
    db.session.add(task)
    db.session.commit()
    return "OK"


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get(task_id)
    if not task:
        return redirect('/')
    
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Todo.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
