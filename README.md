# 📌 OmniBioAI Auth Service

A **production-ready authentication and authorization service** built with FastAPI, providing secure identity management for the OmniBioAI ecosystem.

It supports **JWT authentication, refresh tokens, and role-based access control (RBAC)** across distributed bioinformatics workflows running on local machines, HPC clusters, and cloud infrastructure.

---

# 🚀 Overview

OmniBioAI Auth Service is the central identity layer for the OmniBioAI platform.

It enables:

* Secure user authentication (JWT-based)
* Refresh token management
* Role-Based Access Control (RBAC)
* Multi-service authentication (TES, Studio, LIMS, Control Center)
* Scalable microservice-ready architecture

---

# 🧠 Architecture Role

This service acts as the **single source of truth for identity and access control** across:

* Studio (Electron UI)
* TES (workflow execution engine)
* LIMS (data management system)
* Control Center (system monitoring)
* SDK clients

---

# 🧩 Features

## 🔐 Authentication

* Email/password login
* JWT access tokens
* Refresh token support
* Secure password hashing (bcrypt)

## 🛡️ Authorization

* Role-Based Access Control (RBAC)
* Permission-based access control
* Middleware-based enforcement

## 🗄️ Database

* MySQL backend
* SQLAlchemy ORM
* Auto table creation support

## ⚙️ Architecture

* FastAPI async backend
* Modular service structure
* Clean separation of concerns
* Production-ready codebase

---

# 🏗️ Project Structure

```
app/
├── main.py                  # FastAPI entrypoint
├── core/                   # Security + config
├── db/                     # Database models + session
├── api/                    # API routes + dependencies
├── services/              # Business logic
├── schemas/               # Pydantic models
└── rbac.py                # Permission system
```

---

# ⚙️ Tech Stack

* FastAPI
* MySQL
* SQLAlchemy
* JWT (python-jose)
* Passlib (bcrypt)
* Uvicorn

---

# 📦 Installation

## 1. Clone repository

```bash
git clone git@github.com:man4ish/omnibioai-auth.git
cd omnibioai-auth
```

---

## 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create `.env` file:

```env
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
DB_NAME=omnibioai

SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 5. Run MySQL

Ensure MySQL is running and database exists:

```sql
CREATE DATABASE IF NOT EXISTS omnibioai;
```

---

## 6. Start server

```bash
uvicorn app.main:app --reload --port 8001
```

---

# 📡 API Endpoints

## 🔐 Auth

### Login

```
POST /auth/login
```

**Request**

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**Response**

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

### Refresh Token

```
POST /auth/refresh
```

---

## 🧑 Users (future extension)

```
GET /users/me
```

---

# 🔐 Security Model

* Passwords hashed using bcrypt
* JWT signed using HS256
* Short-lived access tokens (15 min)
* Refresh token rotation support (planned extension)
* RBAC-based permission enforcement

---

# 🧬 RBAC Model

Roles:

* admin
* researcher
* hpc_user
* viewer

Permissions:

* workflow:run
* workflow:cancel
* dataset:read
* dataset:write
* hpc:submit

---

# 🧪 Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 🔗 Integration Targets

This service integrates with:

* Workflow execution engine (TES)
* Electron desktop client (Studio)
* Bioinformatics pipelines
* Cloud/HPC job schedulers

---

# 🚧 Future Enhancements

* OAuth2 (Google/GitHub login)
* Multi-tenant support (lab-level isolation)
* Redis session caching
* Audit logging
* Rate limiting
* Admin dashboard API
* Service-to-service authentication

---

# 🧠 Design Philosophy

This service is designed as:

> A lightweight, scalable identity backbone for distributed scientific computing systems.

---

# 👤 Author

Built as part of the **OmniBioAI ecosystem**
Focused on reproducible, scalable bioinformatics workflows.
