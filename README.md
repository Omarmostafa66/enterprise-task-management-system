# 🚀 Enterprise Task Management System

A modern enterprise-grade task and project management platform built with **FastAPI**, featuring **JWT Authentication**, **Role-Based Access Control (RBAC)**, workflow validation, interactive dashboard UI, and real-time task monitoring.

---

# 📌 Overview

This project is a backend-driven task management system designed for enterprise workflow environments.

The platform allows administrators, project managers, and employees to collaborate through projects and tasks while enforcing secure access control and valid workflow transitions.

---

# ✨ Features

## 🔐 Authentication & Security
- JWT Authentication
- Secure Password Hashing
- OAuth2 Password Flow
- Role-Based Access Control (RBAC)

---

## 👥 User Roles

### 🛡️ Admin
- Manage projects
- Create and delete tasks
- Full system access

### 📋 Project Manager
- Assign and monitor tasks
- Update task statuses
- Track workflow progress

### 👨‍💻 Employee
- View assigned tasks
- Update task status only

---

## 📂 Project Management
- Create projects
- Update projects
- Delete projects
- Project listing and tracking

---

## ✅ Task Management
- Create tasks
- Update tasks
- Delete tasks
- Assign priorities
- Workflow status tracking

---

## 🔄 Workflow Validation

The system enforces valid task lifecycle transitions:

```text
To Do → In Progress → Done
```

Invalid transitions are automatically rejected.

Example:

```text
Done → To Do ❌
```

---

# 🎨 Interactive Dashboard UI

The frontend dashboard includes:

- Dynamic Role-Based UI
- Workflow Progress Tracking
- Real-Time Statistics
- Search & Filtering
- Responsive Enterprise Design
- Toast Notifications
- Animated Components
- Status Monitoring

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- OAuth2
- Redis

---

## Frontend
- HTML5
- CSS3
- Vanilla JavaScript

---

## Tools
- Swagger UI
- Git & GitHub
- Uvicorn

---

# 📁 Project Structure

```text
enterprise-task-management-system/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── static/
├── templates/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Omarmostafa66/enterprise-task-management-system.git
```

---

## 2️⃣ Navigate Into Project

```bash
cd enterprise-task-management-system
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run The Project

```bash
uvicorn app.main:app --reload
```

---

# 🌐 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 🔑 Authentication Example

## Register User

```json
{
  "email": "admin@test.com",
  "full_name": "System Admin",
  "role": "admin",
  "password": "123456"
}
```

---

## Login Response

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "role": "admin"
}
```

---

# 🧪 Testing

The project includes:
- Authentication Tests
- RBAC Tests
- Workflow Validation Tests
- API Endpoint Tests

Run tests using:

```bash
pytest
```

---

# 🔒 RBAC Validation

| Action | Admin | Project Manager | Employee |
|---|---|---|---|
| Create Project | ✅ | ❌ | ❌ |
| Create Task | ✅ | ✅ | ❌ |
| Update Task | ✅ | ✅ | ✅ |
| Delete Task | ✅ | ❌ | ❌ |

---

# 📊 Workflow Example

```text
To Do
   ↓
In Progress
   ↓
Done
```

---

# 📈 Future Improvements

- Kanban Board
- Real-Time Notifications
- Team Collaboration
- Charts & Analytics
- Dark/Light Mode
- Task Deadlines
- Email Notifications
- Drag & Drop Tasks

---

# 👨‍💻 Author

## Omar Mostafa

Backend Developer | FastAPI Enthusiast | AI & Full Stack Learner

GitHub:
https://github.com/Omarmostafa66

---

# ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.