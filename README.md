# Task Manager Web App 📝

## 📌 Overview

This is a **full-featured Task Manager Web Application** built using Flask. It allows users to securely manage their daily tasks with authentication, task filtering, and status tracking.

---

## 🚀 Features

* 🔐 User Signup & Login (with password hashing)
* ➕ Add tasks
* ❌ Delete tasks
* ✅ Mark tasks as complete/incomplete
* ⭐ Mark tasks as important
* 🔍 Filter tasks:

  * All tasks
  * Important tasks
  * Completed tasks
  * In-progress tasks
* 👤 User-specific task management

---

## 🛠️ Tech Stack

* Python
* Flask
* SQLite (Database)
* SQLAlchemy (ORM)
* Flask-Bcrypt (Password hashing)
* HTML, CSS

---

## ⚙️ How It Works

### 1️⃣ Authentication

* Users can **sign up and log in**
* Passwords are securely stored using hashing

### 2️⃣ Task Management

* Each user has their own tasks
* Tasks can be:

  * Marked as done
  * Marked as important

### 3️⃣ Filtering

Users can view:

* Important tasks
* Completed tasks
* Tasks in progress

---

## ▶️ How to Run

### Step 1: Install dependencies

```bash
pip install flask flask_sqlalchemy flask_bcrypt
```

---

### Step 2: Run the app

```bash
python app.py
```

---

### Step 3: Open in browser

```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```bash
task-manager/
│── app.py
│── templates/
│   │── index.html
│   │── login.html
│   │── signup.html
│── static/
│   │── style.css
│── instance/
│   │── final_tasks.db
```

---

## ⚠️ Important Notes

* Database file (`final_tasks.db`) is not included in the repository
* It will be automatically created when you run the app
* Make sure your browser allows cookies (for session login)

---

## 🔮 Future Improvements

* Add task deadlines
* Add notifications/reminders
* Improve UI with modern frameworks
* Deploy online (Render/Heroku)

---

## 👨‍💻 Author

Jyotirmaya Swain
