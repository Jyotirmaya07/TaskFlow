# TaskFlow — Task Manager Web App 📝

A modern task management web application built with Flask that helps users organize, track, and manage their daily tasks through a clean productivity dashboard.

## 📌 Overview

TaskFlow provides a simple workspace where users can securely manage their tasks, track progress, update task status, and filter tasks based on their current needs.

The application includes user authentication, task CRUD operations, priority management, categories, due dates, progress tracking, and a responsive dashboard interface.

---

## 🚀 Features

### 🔐 User Authentication
- User signup and login
- Password hashing using Flask-Bcrypt
- Session-based authentication
- User-specific task management
- Logout functionality

### 📋 Task Management
- Create new tasks
- Edit existing tasks
- Delete tasks
- Change task status
- Mark tasks as completed
- Assign task priority
- Add task categories
- Set due dates
- Add optional task descriptions

### 🔍 Task Filtering
Tasks can be filtered by:

- All Tasks
- To Do
- In Progress
- Completed
- High Priority

### 📊 Productivity Dashboard
- Overall task completion percentage
- Total completed tasks
- To Do task count
- In Progress task count
- Completed task count
- Overdue task count
- Current date display

### 🎨 User Interface
- Clean and modern dashboard
- Responsive layout
- Separate login and signup interfaces
- Task status and priority indicators
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

---

## ⚙️ How It Works

### 1️⃣ Authentication

Users can create an account and log in securely.

Passwords are hashed using **Flask-Bcrypt** before being stored in the database.

### 2️⃣ Task Creation

After logging in, users can create tasks with:

- Title
- Description
- Priority
- Category
- Due date

### 3️⃣ Task Tracking

Each task can be moved between different states:

- To Do
- In Progress
- Completed

Users can also edit or delete their tasks.

### 4️⃣ Dashboard

The dashboard provides an overview of task progress and displays statistics based on the user's tasks.

---

## ▶️ How to Run

### Step 1: Clone the repository

```bash
git clone https://github.com/Jyotirmaya07/TaskFlow.git
cd TaskFlow
