# Project Overview

Build and deploy a Python-based microservices system using **FastAPI** and **PostgreSQL** with **Docker** and **GitHub Actions**.

Learn service communication, automation, and local deployment management with modern async Python frameworks.

---

## Project Structure

```
microservices-project/
├── user-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
├── task-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
├── gateway-service/
│   ├── app/
│   │   ├── main.py
│   │   └── routes.py
│   ├── requirements.txt
│   └── Dockerfile
├── database/
│   ├── init-scripts/
│   │   ├── 01-init-userdb.sql
│   │   └── 02-init-taskdb.sql
│   └── docker-compose-db.yml
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.staging.yml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── scripts/
│   ├── deploy.py
│   ├── health_check.py
│   ├── migrate.py
│   └── setup_env.py
└── README.md
```

---

## Phase 1: Core Setup

### 1. FastAPI Services Development

Create **3 async FastAPI services** with proper project structure:

- **User Service** – Handles authentication, user registration/login with JWT tokens.
- **Task Service** – Manages CRUD operations for to-do items with user ownership.
- **Gateway Service** – Aggregates and routes requests using async HTTP client.

---

### 2. PostgreSQL Database Setup

- Each service connects to separate PostgreSQL databases for **data isolation**.
- Use **SQLAlchemy** with async support for database operations.
- Implement **Pydantic** models for request/response validation.
- Create **database migration scripts** for schema management.

---

### 3. Docker Containerization

- Write **Dockerfile** for each FastAPI service using **Python 3.11+**.
- Create multi-database **Docker Compose** setup with separate PostgreSQL containers.
- Configure service networking for inter-service communication.
- Set up **environment variables** for database connections and service URLs.

---

### 4. Nginx Reverse Proxy

- Configure **Nginx** to route traffic to the gateway service.
- Implement **load balancing** if multiple gateway instances.
- Add static file serving capabilities for future frontend integration.
- Configure **CORS** headers for API access.

---

### 5. Service Communication

- Services communicate via **HTTP/JSON APIs** using async requests.
- Implement **service discovery** using Docker Compose service names.
- Add **retry logic** and **timeout handling** for resilient communication.
- Create **health check endpoints** for all services.
