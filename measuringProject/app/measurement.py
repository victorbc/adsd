from datetime import datetime
from flask import Flask, request, json, jsonify, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
from timer import Timer
import psutil
import os


app = Flask(__name__)
app.config.from_pyfile('measurement.cfg')
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/')
def show_all():
    return render_template('show_all.html',
        todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    )


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    for todo in Todo.query.all():
        todo.done = ('done.%d' % todo.id) in request.form
    flash('Updated status')
    db.session.commit()
    return redirect(url_for('show_all'))


@app.route('/benchmark/read/<query_title>', methods=['GET'])
def benchmark_read(query_title):
    response = dict()
    if request.method == 'GET':
        # get pid of current process and create Process object
        p = psutil.Process(os.getpid())
        # first read is equal to 0.0
        # cpu_usage = p.cpu_percent()
        # Initialize total timer
        with Timer() as total_time:
            with Timer() as db_time:
                todo = Todo.query.filter_by(title=query_title).first()
            # this call influences the total time taken by the call
            response['db_time'] = db_time.secs
        # total time taken by request
        response['total_time'] = total_time.secs
        # CPU usage since last time we called p.cpu_percent()
        response['server_cpu_usage'] = p.cpu_percent(interval=0.1) / psutil.cpu_count()
        # memory usage of process.
        response['server_memory_usage'] = p.memory_info()[0]
        # whole OS CPU usage
        response['so_cpu_usage'] = psutil.cpu_percent(interval=0.1) / psutil.cpu_count()
        # whole OS memory usage
        mem = psutil.virtual_memory()
        response['so_memory_usage'] = psutil.virtual_memory().used

    return jsonify(response)


@app.route('/benchmark/write', methods=['POST'])
def benchmark_write():
    response = dict()
    if request.method == 'POST':
        # get pid of current process and create Process object
        p = psutil.Process(os.getpid())
        # first read is equal to 0.0
        # cpu_usage = p.cpu_percent()
        # Initialize total timer
        with Timer() as total_time:
            # Get request json body
            data = request.json
            # Create object to be inserted into DB
            todo = Todo(data['title'], data['text'])
            # Insert data into DB
            with Timer() as db_time:
                db.session.add(todo)
                db.session.commit()
            response['db_time'] = db_time.secs

        response['total_time'] = total_time.secs
        # CPU usage since last time we called p.cpu_percent()
        response['server_cpu_usage'] = p.cpu_percent(interval=0.1) / psutil.cpu_count()
        # memory usage of process.
        response['server_memory_usage'] = p.memory_info()[0]
        # whole OS CPU usage
        response['so_cpu_usage'] = psutil.cpu_percent(interval=0.2) / psutil.cpu_count()
        # whole OS memory usage
        mem = psutil.virtual_memory()
        response['so_memory_usage'] = psutil.virtual_memory().used

    return jsonify(response)

if __name__ == '__main__':
    app.run()
