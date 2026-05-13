# 🚀 Enterprise Task Management System

A scalable enterprise-grade task and project management platform built with modern backend architecture using FastAPI.

The system provides secure authentication, role-based access control, workflow validation, Redis caching, monitoring tools, and a responsive dashboard interface designed for real-world enterprise environments.

---

# 📌 Project Overview

Managing projects inside companies often becomes difficult when teams grow larger.

Tasks may get lost.
Permissions become unclear.
Managers struggle to track progress.
System performance decreases as data grows.

This project solves those challenges by providing a centralized platform where administrators, project managers, and employees can collaborate securely and efficiently.

The platform focuses on:

* Security
* Performance
* Scalability
* Clean Architecture
* Enterprise Workflow Management

---

# ✨ Core Features

## 🔐 Authentication & Security

The system uses JWT-based authentication with secure password hashing and protected API access.

### Included Security Features

* JWT Authentication
* OAuth2 Password Flow
* Password Hashing
* Role-Based Access Control (RBAC)
* Protected Routes
* Environment Variable Security
* Self-Demotion Prevention
* Last Admin Protection
* Automatic Default Admin Creation

---

# 👥 User Roles & Permissions

## 🛡️ Admin

Full system control.

### Admin Capabilities

* Create and manage projects
* Create, update, and delete tasks
* Manage users and roles
* View audit logs
* Access monitoring information
* Control system permissions

---

## 📋 Project Manager

Responsible for managing team workflows.

### Project Manager Capabilities

* Create tasks
* Assign tasks to employees
* Track task progress
* Update workflow status
* Monitor project activities

---

## 👨‍💻 Employee

Focused task access.

### Employee Capabilities

* View assigned tasks only
* Update personal task status
* Track task progress

---

# 📂 Project Management

The platform provides complete project lifecycle management.

### Supported Operations

* Create Projects
* Update Projects
* Delete Projects
* Track Project Progress
* Assign Team Members

---

# ✅ Task Management

Tasks are the core component of the system.

### Task Features

* Create Tasks
* Update Tasks
* Delete Tasks
* Assign Priorities
* Deadline Tracking
* Status Management
* Role-Based Task Access

---

# 🔄 Workflow Validation

The system enforces valid workflow transitions to maintain logical task progression.

### Valid Workflow

```text
To Do → In Progress → Done
```

### Invalid Workflow

```text
Done → To Do ❌
```

Invalid transitions are automatically rejected by the backend validation layer.

---

# ⚡ Performance Optimization

To improve performance and reduce database load, the project integrates Redis caching.

## Redis Features

* Redis Cache Layer
* Cache HIT / MISS Tracking
* Faster API Responses
* Reduced Database Queries
* Cache Invalidation

### Cache Example

#### First Request

```text
Cache MISS
```

#### Second Request

```text
Cache HIT
```

This demonstrates that repeated requests are served directly from Redis instead of querying MySQL again.

---

# 📈 Monitoring & Logging

Enterprise systems require continuous monitoring and debugging capabilities.

The project includes:

* Structured Logging
* Request Monitoring
* Prometheus Metrics
* API Performance Tracking
* Docker Health Checks

### Metrics Endpoint

```text
http://localhost:8000/metrics
```

### Monitored Information

* Request Duration
* API Usage
* Cache Performance
* Application Health
* Request Logs

---

# 🎨 Interactive Dashboard UI

The frontend dashboard provides a responsive enterprise experience.

## Dashboard Features

* Dynamic Role-Based Interface
* Workflow Tracking
* Real-Time Statistics
* Search & Filtering
* Responsive Layout
* Toast Notifications
* Status Monitoring
* User Management Panel
* Audit Logs Dashboard

---

# 🛠️ Technology Stack

## Backend Technologies

* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* Redis
* JWT Authentication
* OAuth2
* Prometheus

---

## Frontend Technologies

* HTML5
* CSS3
* Vanilla JavaScript

---

## DevOps & Development Tools

* Docker
* Docker Compose
* Swagger UI
* Git & GitHub
* Uvicorn

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

# 🧠 Architecture Design

The project follows a layered enterprise architecture to improve scalability and maintainability.

## Main Layers

### Routers

Handle API endpoints and incoming requests.

### Services

Contain business logic and workflow processing.

### Models

Represent database tables using SQLAlchemy ORM.

### Schemas

Validate request and response data using Pydantic.

### Dependencies

Handle authentication and shared dependencies.

### Utils

Contain helper utilities and reusable functions.

This structure improves:

* Code organization
* Scalability
* Maintainability
* Separation of Concerns

---

# ⚙️ Installation Without Docker

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Omarmostafa66/enterprise-task-management-system.git
```

## 2️⃣ Navigate Into Project

```bash
cd enterprise-task-management-system
```

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

## 4️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 6️⃣ Configure Environment Variables

Create a `.env` file:

```env
SQLALCHEMY_DATABASE_URL=mysql+pymysql://root:@localhost:3306/task_db

REDIS_HOST=localhost
REDIS_PORT=6379

SECRET_KEY=super_secure_enterprise_secret_key_2026
ALGORITHM=HS256
```

## 7️⃣ Run The Application

```bash
uvicorn app.main:app --reload
```

---

# 🐳 Docker Deployment

Docker simplifies project setup and deployment.

## Run Using Docker

```bash
docker compose up --build
```

---

# 🌐 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Prometheus Metrics:

```text
http://127.0.0.1:8000/metrics
```

---

# 🔑 Default Admin Account

The system automatically creates a default admin account during first startup if no administrator exists.

## Default Credentials

```text
Email: admin@system.com
Password: admin123
```

It is recommended to change the default password after deployment.

---

# 🔑 Authentication Example

## Register User

```json
{
  "email": "employee@test.com",
  "full_name": "John Doe",
  "password": "123456"
}
```

All new users are assigned the Employee role by default.

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

The project includes automated tests for critical system functionality.

## Included Tests

* Authentication Tests
* RBAC Tests
* Workflow Validation Tests
* Redis Cache Tests
* API Endpoint Tests

## Run Tests

```bash
pytest
```

---

# 🔒 RBAC Validation Table

| Action          | Admin | Project Manager | Employee |
| --------------- | ----- | --------------- | -------- |
| Create Project  | ✅     | ❌               | ❌        |
| Create Task     | ✅     | ✅               | ❌        |
| Update Task     | ✅     | ✅               | ✅        |
| Delete Task     | ✅     | ❌               | ❌        |
| Manage Users    | ✅     | ❌               | ❌        |
| View Audit Logs | ✅     | ❌               | ❌        |

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

# 🔐 Security Highlights

* JWT Authentication
* Secure Password Hashing
* Protected API Endpoints
* Role-Based Authorization
* Environment Variable Protection
* Self-Demotion Prevention
* Last Admin Protection
* Automatic Admin Initialization

---

# 🚀 Future Improvements

Planned future enhancements include:

* Kanban Board
* Real-Time Notifications
* Email Notifications
* Team Collaboration Tools
* Charts & Analytics
* Dark / Light Mode
* Drag & Drop Tasks
* Advanced Reporting

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
