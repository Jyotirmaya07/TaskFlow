# TaskFlow — Task Manager Web App 📝

A modern Flask-based task management web application for organizing, tracking, and managing daily tasks through a productivity-focused dashboard.

---

## 📌 Overview

TaskFlow provides users with a personal workspace where they can create, organize, update, and track their tasks efficiently.

The application includes secure user authentication, task CRUD operations, priority management, categories, due dates, status tracking, task filtering, and a productivity dashboard with dynamic task statistics.

---

## 🚀 Features

### 🔐 User Authentication

- User signup and login
- Password hashing using Flask-Bcrypt
- Session-based authentication
- User-specific task management
- Logout functionality
- Protected task operations

### 📋 Task Management

Users can:

- Create new tasks
- Edit existing tasks
- Delete tasks
- Change task status
- Mark tasks as completed
- Assign task priorities
- Add task categories
- Set due dates
- Add optional descriptions

### 📊 Task Status

Each task can be managed through three states:

- To Do
- In Progress
- Completed

Tasks can be moved between different states directly from the dashboard.

### 🔍 Task Filtering

Tasks can be filtered by:

- All Tasks
- To Do
- In Progress
- Completed
- High Priority

### 📈 Productivity Dashboard

The dashboard provides an overview of the user's productivity, including:

- Overall completion percentage
- Total tasks
- Completed tasks
- To Do task count
- In Progress task count
- Overdue task count
- Current date

### 🎨 User Interface

- Clean and modern dashboard
- Responsive layout
- Dedicated login and signup pages
- Task status indicators
- Priority indicators
- Category labels
- Due-date indicators
- Responsive task management interface
- Mobile-friendly design

---

## 🛠️ Tech Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt

### Database

- SQLite

### Frontend

- HTML5
- CSS3
- Bootstrap 5

### Development Tools

- Git
- GitHub
- VS Code

---

## ⚙️ How It Works

### 1. User Authentication

Users can create an account and log in to their personal TaskFlow workspace.

Passwords are hashed using **Flask-Bcrypt** before being stored in the database.

Session-based authentication ensures that users can access only their own workspace and tasks.

### 2. Task Creation

After logging in, users can create tasks by providing:

- Task title
- Description
- Priority
- Category
- Due date

### 3. Task Tracking

Tasks can be moved between different states:

**To Do → In Progress → Completed**

Users can also edit or delete existing tasks.

### 4. Task Filtering

The dashboard allows users to quickly view tasks based on their status or priority.

### 5. Productivity Dashboard

TaskFlow dynamically calculates task statistics and displays:

- Overall completion percentage
- Total tasks
- Completed tasks
- To Do tasks
- In-progress tasks
- Overdue tasks

This gives users a quick overview of their current workload and progress.

---

## 📁 Project Structure

```text
TaskFlow/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── edit.html
│
├── instance/
│   └── final_tasks.db
│
└── README.md


## 👨‍💻 Author

**Jyotirmaya Swain**

B.Tech — Computer Science Engineering  
Specialization: Artificial Intelligence & Machine Learning
