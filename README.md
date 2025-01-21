# Backend for Our Savior Community Garden

This repository contains the backend code for the "Our Savior Community Garden" project. The backend is built using **FastAPI**, a modern Python framework for creating APIs. It provides endpoints for user authentication, managing schedules, and interacting with a MySQL database.

---

## Key Features

1. **User Authentication**:
   - Login functionality with secure token generation using JWT (JSON Web Tokens).

2. **Schedule Management**:
   - Fetch all schedules.
   - Add new schedules.
   - Edit existing schedules.
   - Delete schedules.

3. **Database**:
   - MySQL is used for storing user and schedule data.
   - Asynchronous database interactions are implemented using `aiomysql`.

4. **Documentation**:
   - Interactive API documentation is available at `/docs` using Swagger UI.

5. **Cross-Origin Resource Sharing (CORS)**:
   - Enabled to allow frontend-backend communication.

---

## Project Structure

```
.
├── app.py             # Main FastAPI application
├── config.py          # Configuration file for environment variables and database
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── .env               # Environment variables (not included in version control)
```

---

## API Overview

- **Authentication**:
  - Login endpoint to generate secure tokens.

- **Schedule Management**:
  - Endpoints to fetch, add, edit, and delete schedules.

---

This backend is designed to be lightweight, scalable, and easy to integrate with the frontend of the project.
