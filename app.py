from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pathlib

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_tasks.db'
app.config['SECRET_KEY'] = 'thisshouldbeareallysecurekey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

print("→ Database will be created at:", pathlib.Path('final_tasks.db').resolve())

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    is_important = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create DB tables if not exist
with app.app_context():
    db.create_all()

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        if User.query.filter_by(username=username).first():
            return "User already exists!"
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Home
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks, username=session.get('username'))

# Add Task
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')
    content = request.form.get('task')
    importance = request.form.get('importance') == 'yes'
    if content:
        task = Task(content=content, is_important=importance, user_id=session['user_id'])
        db.session.add(task)
        db.session.commit()
    return redirect('/')

# Delete Task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect('/login')
    task = Task.query.get(task_id)
    if task and task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

# Toggle Task Status
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    if 'user_id' not in session:
        return redirect('/login')
    task = Task.query.get(task_id)
    if task and task.user_id == session['user_id']:
        task.is_done = not task.is_done
        db.session.commit()
    return redirect('/')

# Filter: Important
@app.route('/important')
def important():
    if 'user_id' not in session:
        return redirect('/login')
    tasks = Task.query.filter_by(user_id=session['user_id'], is_important=True).all()
    return render_template('index.html', tasks=tasks, username=session.get('username'))

# Filter: Completed
@app.route('/completed')
def completed():
    if 'user_id' not in session:
        return redirect('/login')
    tasks = Task.query.filter_by(user_id=session['user_id'], is_done=True).all()
    return render_template('index.html', tasks=tasks, username=session.get('username'))

# Filter: In Progress
@app.route('/inprogress')
def inprogress():
    if 'user_id' not in session:
        return redirect('/login')
    tasks = Task.query.filter_by(user_id=session['user_id'], is_done=False).all()
    return render_template('index.html', tasks=tasks, username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)
