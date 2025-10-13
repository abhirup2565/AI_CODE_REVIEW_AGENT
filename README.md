Perfect! Based on your clarifications, here’s a detailed and structured **`README.md` draft** for your project:

---

# Code PR Review System

⚡ Automate Pull Request Reviews using AI with FastAPI, Celery, and Google Gemini LLM

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Architecture & Workflow](#architecture--workflow)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Setup & Installation](#setup--installation)
8. [Future Perspectives](#future-perspectives)

---

## Project Overview

The **Code PR Review System** allows developers to automatically review pull requests (PRs) in their repositories using AI. The system supports task queuing via **Celery** and **Redis**, stores results in **Supabase Postgres**, and leverages **Google Gemini** via **LangChain** and **LangGraph** for AI-powered code review.

---

## ✨ Features

* User registration and authentication with **JWT (access + refresh tokens)**
* Background task processing for PR analysis using Celery
* AI-generated code review, including **critical issues** and **non-critical issues**
* Real-time task status tracking
* Stores review results per file and per task in Postgres
* Protected endpoints for authenticated users only

---

## 🧩 Tech Stack

| Component        | Technology                              |
| ---------------- | --------------------------------------- |
| Backend          | FastAPI                                 |
| Background Tasks | Celery                                  |
| Broker & Backend | Redis (Docker)                          |
| Database         | Supabase Postgres                       |
| AI/LLM           | Google Gemini via LangChain & LangGraph |
| Auth             | JWT (Access + Refresh tokens)           |

---

## 🏗️ Architecture & Workflow

1. 🔹**User Management**

   * Users register via auth/register (email + password).
   * On login (auth/login), an access token (15 min) and refresh token (7 days) are issued.
   * Access tokens are used for authorization in protected endpoints.
   * Refresh tokens are stored in the RefreshToken table and also set in cookies for session continuity.
   * When a refresh token is rotated or invalidated, its revoked flag is set to true in the same table — it’s not stored elsewhere.
   * The BlockAccessToken table only stores access tokens that are explicitly revoked during logout or expired manually.

2. 🔹**Task Creation**

   * Authenticated users call `api/analyze-pr` with `url`, `pr_number`, and optional `token`.
   * A Celery background task (`analyze_pr_task`) is queued via Redis.
   * Task status (`submitted`) and `task_id` is returned immediately.

3. 🔹**Task Processing**

   * Celery fetches the PR files using GitHub API.
   * Files are chunked (default token size: 1000) and passed to **Google Gemini LLM**.
   * AI generates a summary including **critical issues** (bugs) and **non-critical issues** (styling, maintenance).
   * Results are formatted using **Pydantic** and stored in `TaskResult` and `FileResult` tables in Postgres.

4. 🔹**Status Tracking & Results**

   * `api/status/{task_id}` returns real-time task status.
   * `api/user_tasks` returns all tasks associated with the logged-in user.
   * `api/results/{task_id}` fetches the completed AI review results from the database.

5. 🔹**Token Management**

   * `auth/refresh` rotates refresh tokens and issues new access tokens.
   * `auth/logout` revokes refresh tokens and blocks access tokens.

---

## 🔌 API Endpoints

| Endpoint                 | Method | Description                      | Request Body / Params                                     | Response Example                                                                                            |
| ------------------------ | ------ | -------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `/auth/register`         | POST   | Register a new user              | `{ "email": "user@example.com", "password": "string" }`   | `{ "message": "User created successfully" }`                                                                |
| `/auth/login`            | POST   | Login and get tokens             | `{ "email": "user@example.com", "password": "string" }`   | `{ "access_token": "...", "refresh_token": "...", "token_type": "bearer", "refresh_expiry": "YYYY-MM-DD" }` |
| `/auth/refresh`          | POST   | Refresh access and refresh token | `{ "refresh_token": "..." }`                              | `{ "access_token": "...", "refresh_token": "...", "token_type": "bearer", "refresh_expiry": "YYYY-MM-DD" }` |
| `/auth/logout`           | POST   | Logout user                      | `{ "refresh_token": "..." }`                              | `{ "message": "Logout successful" }`                                                                        |
| `/api/analyze-pr`        | POST   | Create AI code review task       | `{ "url": "...", "pr_number": 123, "token": "optional" }` | `{ "task_id": "abc123", "status": "submitted" }`                                                            |
| `/api/status/{task_id}`  | GET    | Get real-time task status        | URL param: `task_id`                                      | `{ "task_id": "abc123", "status": "completed" }`                                                            |
| `/api/user_tasks`        | GET    | List tasks for logged-in user    | JWT required                                              | `[{"task_id": "abc123", "status": "completed"}]`                                                            |
| `/api/results/{task_id}` | GET    | Get AI review result             | URL param: `task_id`                                      | `{ "task_id": "abc123", "summary": {...}, "files": [...] }`                                                 |

---

## 🗄️ Database Schema

### Users Table

| Column          | Type     | Description           |
| --------------- | -------- | --------------------- |
| id              | int (PK) | User ID               |
| email           | string   | User email            |
| hashed_password | string   | Hashed password       |
| created_at      | datetime | Account creation time |

### RefreshToken Table

| Column     | Type                | Description         |
| ---------- | ------------------- | ------------------- |
| id         | int (PK)            | Token ID            |
| user_id    | int (FK → Users.id) | Owner user          |
| token      | string              | JWT token           |
| revoked    | bool                | If token is revoked |
| created_at | datetime            | Creation timestamp  |
| expires_at | datetime            | Expiry timestamp    |

### BlockAccessToken Table

| Column     | Type     | Description            |
| ---------- | -------- | ---------------------- |
| id         | int (PK) | Token ID               |
| token      | string   | Access token           |
| blocked_at | datetime | When token was blocked |

### TaskResult Table

| Column     | Type                | Description                                   |
| ---------- | ------------------- | --------------------------------------------- |
| id         | int (PK)            | Task ID                                       |
| user_id    | int (FK → Users.id) | Owner user                                    |
| task_id    | string              | Celery task ID                                |
| status     | string              | submitted / completed                         |
| summary    | json                | Task summary (critical & non-critical issues) |
| created_at | datetime            | Task creation timestamp                       |
| updated_at | datetime            | Last updated timestamp                        |

### FileResult Table

| Column   | Type                     | Description                |
| -------- | ------------------------ | -------------------------- |
| id       | int (PK)                 | File result ID             |
| task_id  | int (FK → TaskResult.id) | Related task               |
| filename | string                   | File name in PR            |
| content  | text                     | File content               |
| issues   | json                     | AI reported issues in file |

---

## ⚙️ Setup & Installation

1. Clone the repo:

   ```bash
   git clone <repo_url>
   cd code-pr-review-system
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```env
   DATABASE_URL=<supabase_postgres_url>
   JWT_SECRET=<secret_key>
   ```

4. Run FastAPI:

   ```bash
   uvicorn main:app --reload
   ```

5. Start Celery worker (if using your local setup):

   ```bash
   celery -A workers.tasks.celery_app worker --loglevel=info
   ```

---

## 🚀 Future Perspectives

* Integrate with a **frontend dashboard** for better visualization
* Add **cron job** to clean expired tokens from the database
* Extend AI reviews to support **multi-repo batch analysis**
* Implement **notification system** for completed tasks

---
