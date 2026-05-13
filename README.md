# 🚀 Enterprise Task Management System

A modern enterprise-grade task and project management platform built with **FastAPI**, featuring **JWT Authentication**, **Role-Based Access Control (RBAC)**, Redis caching, Docker containerization, workflow validation, monitoring, and an interactive dashboard UI.

---

# 📌 Overview

This project is a backend-driven task management system designed for enterprise workflow environments.

The platform allows administrators, project managers, and employees to collaborate through projects and tasks while enforcing secure access control, audit logging, workflow validation, and high-performance caching.

---

# ✨ Features

## 🔐 Authentication & Security
- JWT Authentication
- Secure Password Hashing
- OAuth2 Password Flow
- Role-Based Access Control (RBAC)
- Environment Variable Security (.env)
- Protected Admin Operations
- Last Admin Protection
- Self-Demotion Prevention
- Automatic Default Admin Creation

---

## ⚡ Performance & Monitoring
- Redis Caching
- Cache Invalidation
- Cache HIT / MISS Logging
- Structured Logging
- Prometheus Metrics
- Request Performance Monitoring
- Docker Health Checks

---

## 👥 User Roles

### 🛡️ Admin
- Manage projects
- Create and delete tasks
- Manage users
- Change user roles
- View audit logs
- Full system access

### 📋 Project Manager
- Assign and monitor tasks
- Update task statuses
- Track workflow progress
- Create tasks

### 👨‍💻 Employee
- View assigned tasks
- Update assigned tasks only

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
- Role-based task access

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
- User Management Panel
- Audit Logs Dashboard

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- JWT Authentication
- OAuth2
- Redis
- Prometheus

---

## Frontend
- HTML5
- CSS3
- Vanilla JavaScript

---

## DevOps & Tools
- Docker
- Docker Compose
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
│   ├── dependencies/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
├── frontend/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation (Without Docker)

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

## 6️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
SQLALCHEMY_DATABASE_URL=mysql+pymysql://root:@localhost:3306/task_db

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Security
SECRET_KEY=super_secure_enterprise_secret_key_2026

# JWT Algorithm
ALGORITHM=HS256
```

---

## 7️⃣ Run The Project

```bash
uvicorn app.main:app --reload
```

---

## 8️⃣ Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

## 9️⃣ Run Frontend

Open:

```text
frontend/index.html
```

Recommended:

Use VS Code Live Server.

---

# 🐳 Run The Project Using Docker

## 1️⃣ Make Sure Docker Desktop Is Installed

Download Docker Desktop:

[Docker Desktop](https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com)

---

## 2️⃣ Start Docker Desktop

Make sure Docker is running before executing the next command.

---

## 3️⃣ Build And Start Containers

```bash
docker compose up --build
```

---

## 4️⃣ Access The Application

### Swagger API Documentation

```text
http://localhost:8000/docs
```

### Prometheus Metrics

```text
http://localhost:8000/metrics
```

---

## 5️⃣ Run Frontend

Open:

```text
frontend/index.html
```

Recommended:

Use VS Code Live Server.

---

# 🌐 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 🔑 Default Admin Account

The system automatically creates a default admin account on first startup if no admin exists.

## Default Admin Credentials

```text
Email: admin@system.com
Password: admin123
```

Important:

After creating your own admin account, it is recommended to deactivate or change the password of the default admin account.

---

# 🔑 Authentication Example

## Register User

All newly registered users are automatically assigned the Employee role.

```json
{
  "email": "employee@test.com",
  "full_name": "John Doe",
  "password": "123456"
}
```

---

## Login Response

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "role": "employee"
}
```

---

# 🧪 Testing

The project includes:
- Authentication Tests
- RBAC Tests
- Workflow Validation Tests
- Redis Cache Tests
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
| Manage Users | ✅ | ❌ | ❌ |
| View Audit Logs | ✅ | ❌ | ❌ |

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

# ⚡ Redis Cache Example

### First Request

```text
Cache MISS
```

### Second Request

```text
Cache HIT
```

This confirms that task data is being served directly from Redis cache for improved performance.

---

# 📈 Monitoring

Prometheus metrics are available at:

```text
http://localhost:8000/metrics
```

The system tracks:
- Request duration
- API usage
- Cache performance
- Application health
- Request logs

---

# 🔐 Security Features

- JWT Token Authentication
- Password Hashing
- Environment Variable Protection
- Last Admin Protection
- Self-Demotion Prevention
- Role-Based Permissions
- Protected Endpoints
- Automatic Default Admin Creation

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

[Omarmostafa66 GitHub](https://github.com/Omarmostafa66?utm_source=chatgpt.com)

---

# ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.