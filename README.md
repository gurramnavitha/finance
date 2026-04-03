# Finance Data Processing and Access Control System

This is a complete full-stack web application built for managing financial records, utilizing **FastAPI** for a high-performance backend, **Microsoft SQL Server** as the database layer with `pyodbc` & `sqlalchemy`, and **Streamlit** for the frontend user interface. The system employs secure JWT authentication and Role-Based Access Control (RBAC).

## End-to-End Architecture

The project adopts a decoupled architecture where the API Backend acts as the single source of truth for the Database, applying strict validations and access limits before sending summarized responses to the Streamlit Client.

```
┌─────────────────┐       HTTP JSON       ┌────────────────────────┐
│                 │   (RESTful API + JWT) │                        │
│ Streamlit UI    │◄─────────────────────►│ FastAPI Backend        │
│ (frontend/)     │                       │ (app/)                 │
│                 │                       │                        │
└─────────────────┘                       └───────────┬────────────┘
                                                      │
                                                      │ SQLAlchemy ORM
                                                      │ (pyodbc)
                                                      ▼
                                          ┌────────────────────────┐
                                          │ Microsoft SQL Server   │
                                          │ (Records, Users, etc)  │
                                          └────────────────────────┘
```

### 1. Database Layer (Microsoft SQL Server)
The data is persisted securely in a local MS SQL Server instance (`@SAIDEVMACHINE\SQLEXPRESS`). The database contains exactly two tables: `users` and `records`, configured with strict Foreign Keys.

### 2. Backend Layer (FastAPI)
The backend service (`uvicorn app.main:app`) handles all logic:
- **Routing & Validation**: `pydantic` heavily validates that dates, float values, strings, and types are valid (e.g. enforcing "income" or "expense" via enumerations).
- **Authentication**: Using `OAuth2PasswordBearer`, a route login issues an encrypted JWT token using `passlib` and `bcrypt`.
- **Authorization (RBAC)**: Custom dependencies ensure tokens match the user roles (`Viewer`, `Analyst`, `Admin`). If a `Viewer` tries to POST a record, they hit an automatic `HTTP 403 Forbidden` wall.

### 3. Frontend Layer (Streamlit)
The Streamlit app runs via `streamlit run frontend/app.py`. It uses `st.session_state` to store JWT Tokens upon successful login and subsequently passes headers dynamically like `{"Authorization": "Bearer ...Token..."}` along with user actions.

---

## Setup & Running Instructions

### 1. Prerequisites
- Python 3.9+
- ODBC Driver 17 for SQL Server installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database configuration
Verify your backend `.env` matches your MS SQL instance. If connecting over Windows Auth, ensure `trusted_connection=yes` is present, or append `UID=username;PWD=password` specifically.

### 4. Running the Backend
From the root directory of the project, run:
```bash
uvicorn app.main:app --reload
```
The FastAPI swagger UI will be available at: http://localhost:8000/docs

### 5. Running the Frontend
In another command prompt, from the root folder, run:
```bash
streamlit run frontend/app.py
```
The Dashboard will be accessible at: http://localhost:8501

### Getting Started (First Login)
Because there is no default Admin user out of the box, you can create one directly using the FastAPI Docs (http://localhost:8000/docs) via the `POST /users/` endpoint. Example JSON body:
```json
{
  "name": "Super Admin",
  "email": "admin@example.com",
  "password": "securepassword",
  "role": "Admin",
  "status": "active"
}
```
Then use `admin@example.com` / `securepassword` to log into the Streamlit Portal!
