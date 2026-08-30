from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date
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

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), default='To Do')
    priority = db.Column(db.String(20), default='Medium')

    due_date = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(50), default='Personal')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

# Create DB tables if not exist
with app.app_context():
    db.create_all()

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return redirect('/signup')

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            username=username,
            password=hashed_pw
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please sign in.", "success")
        return redirect('/login')

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/')

        flash("Invalid username or password.", "error")
        return redirect('/login')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Home / Dashboard
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    tasks = Task.query.filter_by(user_id=user_id).order_by(
        Task.due_date.asc()
    ).all()

    # Task statistics
    total_tasks = len(tasks)

    todo_tasks = sum(
        1 for task in tasks
        if task.status == 'To Do'
    )

    inprogress_tasks = sum(
        1 for task in tasks
        if task.status == 'In Progress'
    )

    completed_tasks = sum(
        1 for task in tasks
        if task.status == 'Completed'
    )

    # Deadline statistics
    overdue_tasks = sum(
        1 for task in tasks
        if task.due_date
        and task.due_date < date.today()
        and task.status != 'Completed'
    )

    due_today_tasks = sum(
        1 for task in tasks
        if task.due_date == date.today()
        and task.status != 'Completed'
    )

    upcoming_tasks = sum(
        1 for task in tasks
        if task.due_date
        and task.due_date > date.today()
        and task.status != 'Completed'
    )

    # Completion percentage
    progress = (
        round((completed_tasks / total_tasks) * 100)
        if total_tasks > 0
        else 0
    )

    return render_template(
        'index.html',
        tasks=tasks,
        username=session.get('username'),
        total_tasks=total_tasks,
        todo_tasks=todo_tasks,
        inprogress_tasks=inprogress_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        due_today_tasks=due_today_tasks,
        upcoming_tasks=upcoming_tasks,
        progress=progress,
        today=date.today()
    )
# Add Task
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    category = request.form.get('category')

    if title:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None,
            category=category,
            user_id=session['user_id']
        )

        db.session.add(task)
        db.session.commit()

    return redirect('/')

# Edit Task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    task = Task.query.get(task_id)

    # Make sure the task exists and belongs to the logged-in user
    if not task or task.user_id != session['user_id']:
        return redirect('/')

    if request.method == 'POST':

        # Get updated values from the form
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        category = request.form.get('category')
        status = request.form.get('status')
        due_date = request.form.get('due_date')

        print("EDIT FORM DATA:")
        print("Title:", title)
        print("Description:", description)
        print("Priority:", priority)
        print("Category:", category)
        print("Status:", status)
        print("Due Date:", due_date)

        # Update task
        task.title = title
        task.description = description
        task.priority = priority
        task.category = category
        task.status = status

        # Update due date
        if due_date:
            task.due_date = datetime.strptime(
                due_date,
                '%Y-%m-%d'
            ).date()
        else:
            task.due_date = None

        # Save changes
        db.session.commit()

        print("TASK UPDATED SUCCESSFULLY")
        print("NEW STATUS:", task.status)

        return redirect('/')

    # GET request → show edit page
    return render_template(
        'edit.html',
        task=task
    )

# Toggle Task Status
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    task = Task.query.get(task_id)

    if not task or task.user_id != session['user_id']:
        return redirect('/')

    # Change status
    if task.status == 'To Do':
        task.status = 'In Progress'

    elif task.status == 'In Progress':
        task.status = 'Completed'

    elif task.status == 'Completed':
        task.status = 'To Do'

    else:
        task.status = 'To Do'

    db.session.commit()

    return redirect('/')

# Delete Task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    task = Task.query.get(task_id)

    if not task or task.user_id != session['user_id']:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()

    return redirect('/')

# Filter: To Do
@app.route('/todo')
def todo():
    if 'user_id' not in session:
        return redirect('/login')

    tasks = Task.query.filter_by(
        user_id=session['user_id'],
        status='To Do'
    ).order_by(Task.due_date.asc()).all()

    return render_template(
        'index.html',
        tasks=tasks,
        username=session.get('username'),
        total_tasks=len(tasks),
        todo_tasks=len(tasks),
        inprogress_tasks=0,
        completed_tasks=0,
        overdue_tasks=0,
        due_today_tasks=0,
        upcoming_tasks=0,
        progress=0,
        today=date.today()
    )

# Filter: High Priority
@app.route('/important')
def important():
    if 'user_id' not in session:
        return redirect('/login')

    tasks = Task.query.filter_by(
        user_id=session['user_id'],
        priority='High'
    ).order_by(Task.due_date.asc()).all()

    return render_template(
        'index.html',
        tasks=tasks,
        username=session.get('username'),
        total_tasks=len(tasks),
        todo_tasks=sum(1 for task in tasks if task.status == 'To Do'),
        inprogress_tasks=sum(1 for task in tasks if task.status == 'In Progress'),
        completed_tasks=sum(1 for task in tasks if task.status == 'Completed'),
        overdue_tasks=sum(
            1 for task in tasks
            if task.due_date
            and task.due_date < date.today()
            and task.status != 'Completed'
        ),
        due_today_tasks=sum(
            1 for task in tasks
            if task.due_date == date.today()
            and task.status != 'Completed'
        ),
        upcoming_tasks=sum(
            1 for task in tasks
            if task.due_date
            and task.due_date > date.today()
            and task.status != 'Completed'
        ),
        progress=round(
            sum(1 for task in tasks if task.status == 'Completed')
            / len(tasks) * 100
        ) if tasks else 0,
        today=date.today()
    )


# Filter: Completed
@app.route('/completed')
def completed():
    if 'user_id' not in session:
        return redirect('/login')

    tasks = Task.query.filter_by(
        user_id=session['user_id'],
        status='Completed'
    ).order_by(Task.due_date.asc()).all()

    return render_template(
        'index.html',
        tasks=tasks,
        username=session.get('username'),
        total_tasks=len(tasks),
        todo_tasks=0,
        inprogress_tasks=0,
        completed_tasks=len(tasks),
        overdue_tasks=0,
        due_today_tasks=0,
        upcoming_tasks=0,
        progress=100 if tasks else 0,
        today=date.today()
    )


# Filter: In Progress
@app.route('/inprogress')
def inprogress():
    if 'user_id' not in session:
        return redirect('/login')

    tasks = Task.query.filter_by(
        user_id=session['user_id'],
        status='In Progress'
    ).order_by(Task.due_date.asc()).all()

    return render_template(
        'index.html',
        tasks=tasks,
        username=session.get('username'),
        total_tasks=len(tasks),
        todo_tasks=0,
        inprogress_tasks=len(tasks),
        completed_tasks=0,
        overdue_tasks=sum(
            1 for task in tasks
            if task.due_date
            and task.due_date < date.today()
        ),
        due_today_tasks=sum(
            1 for task in tasks
            if task.due_date == date.today()
        ),
        upcoming_tasks=sum(
            1 for task in tasks
            if task.due_date
            and task.due_date > date.today()
        ),
        progress=0,
        today=date.today()
    )

if __name__ == '__main__':
    app.run(debug=True)
