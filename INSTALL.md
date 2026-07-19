# Installation and Setup Guide

This guide provides step-by-step instructions for setting up the Hajj Pilgrims Management System locally for development.

## Prerequisites

Before you begin, ensure the following software is installed on your system:

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Node.js 18+ and npm**
   ```bash
   node --version
   npm --version
   ```

3. **PostgreSQL 16+**
   ```bash
   psql --version
   ```

4. **Git**
   ```bash
   git --version
   ```

5. **Docker and Docker Compose** (optional, for containerized setup)
   ```bash
   docker --version
   docker compose version
   ```

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/ipilgram.git
cd ipilgram
```

---

## 2. PostgreSQL Setup

### Option A: Local PostgreSQL Installation

1. Start the PostgreSQL service if it is not running.

2. Create the database:
   ```sql
   CREATE DATABASE hajj_pilgrims;
   ```

3. Create a database user (or use the default `postgres` user):
   ```sql
   CREATE USER hajj_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE hajj_pilgrims TO hajj_user;
   ```

4. Grant schema permissions:
   ```sql
   \c hajj_pilgrims
   GRANT ALL ON SCHEMA public TO hajj_user;
   ```

### Option B: Docker PostgreSQL (Standalone)

If you only need the database via Docker:

```bash
docker run -d \
  --name hajj_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=hajj_pilgrims \
  -p 5432:5432 \
  postgres:16-alpine
```

---

## 3. Backend Setup

### 3.1 Create and Activate Virtual Environment

```bash
cd backend
python -m venv venv
```

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 3.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.3 Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and edit the following values:

```env
# Database connection string
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hajj_pilgrims

# Generate a strong secret key
SECRET_KEY=<run the command below to generate this>

# Set to True for development
DEBUG=True

# CORS origins (must match the admin portal URL)
CORS_ORIGINS=["http://localhost:5173"]

# Google Gemini API key (optional, for AI features)
GEMINI_API_KEY=

# Firebase credentials path (optional, for push notifications)
FIREBASE_CREDENTIALS_PATH=

# Server settings
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

Generate a strong secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output as the value of `SECRET_KEY` in your `.env` file.

### 3.4 Run Database Migrations

```bash
alembic upgrade head
```

This creates all required tables:
- `users` -- Admin and pilgrim accounts
- `refresh_tokens` -- Hashed refresh tokens for JWT rotation
- `flights` -- Flight records
- `accommodations` -- Hotel and accommodation records
- `transports` -- Ground transportation records
- `packages` -- Hajj packages linking flights, accommodations, and transports
- `announcements` -- Announcement templates with placeholder support
- `preferences` -- Pilgrim display and notification preferences
- `notifications` -- System-generated notifications
- `device_tokens` -- FCM device tokens for push notifications

### 3.5 Seed the Admin User

```bash
python seed.py
```

This creates the default admin account:
- Email: `admin@hajj.ng`
- Password: `admin123`
- Role: `admin`

If the user already exists, the script will report "Admin user already exists." and exit without error.

### 3.6 Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now running at `http://localhost:8000`.

Verify with:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "success": true,
  "message": "Service is healthy",
  "data": { "status": "healthy" },
  "errors": null
}
```

### 3.7 Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 4. Frontend Setup (Admin Portal)

**Note**: The React admin portal is for administrative use only. Pilgrims use the Flutter mobile app (in development) and do not interact with this portal.

### 4.1 Install Dependencies

Open a new terminal:

```bash
cd admin-portal
npm install
```

### 4.2 Configure Environment Variables

```bash
cp .env.example .env
```

The default value is sufficient for local development:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 4.3 Start the Development Server

```bash
npm run dev
```

The admin portal is now running at `http://localhost:5173`.

### 4.4 Login

Navigate to `http://localhost:5173` and log in with:

- Email: `admin@hajj.ng`
- Password: `admin123`

### 4.5 Linting

```bash
npm run lint
```

### 4.6 Production Build

```bash
npm run build
```

The output is written to `admin-portal/dist/`.

---

## 5. Docker Setup

### 5.1 Development (Full Stack)

This starts both the PostgreSQL database and the backend API in containers:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

Run migrations inside the running container:

```bash
docker exec -it hajj_api_dev alembic upgrade head
```

Seed the admin user:

```bash
docker exec -it hajj_api_dev python seed.py
```

Stop the containers:

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```

### 5.2 Production

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

This starts:
- A PostgreSQL 16 instance with persistent storage
- The backend API with health checks and restart policy

Set the required environment variables in your shell or in a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=hajj_pilgrims
SECRET_KEY=<strong-secret-key>
CORS_ORIGINS=["https://your-admin-domain.com"]
GEMINI_API_KEY=<your-key>
```

Run migrations in the production container:

```bash
docker exec -it hajj_api_prod alembic upgrade head
```

---

## 6. Running Tests

### 6.1 Backend Tests

From the `backend` directory with the virtual environment activated:

```bash
pytest tests/ -v
```

### 6.2 Integration Test Script

An integration test script is available for testing the full API surface:

```bash
# Ensure the server is running first
python test_all.py
```

This script logs in, exercises all major endpoints, and prints a summary. The server must be running at `http://127.0.0.1:8002` (edit the `BASE` variable in `test_all.py` if your port differs).

---

## 7. Environment Variable Reference

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | -- | PostgreSQL connection string |
| `SECRET_KEY` | Yes | -- | JWT signing key (min 32 characters) |
| `DEBUG` | No | `False` | Enable debug mode |
| `APP_VERSION` | No | `1.0.0` | Application version string |
| `CORS_ORIGINS` | No | `["http://localhost:5173"]` | Allowed CORS origins |
| `GEMINI_API_KEY` | No | `""` | Google Gemini API key |
| `FIREBASE_CREDENTIALS_PATH` | No | `""` | Path to Firebase service account JSON |
| `HOST` | No | `0.0.0.0` | Server bind address |
| `PORT` | No | `8000` | Server port |
| `WORKERS` | No | `2` | Gunicorn worker count |

### Frontend (`admin-portal/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `VITE_API_BASE_URL` | No | `http://localhost:8000/api/v1` | Backend API base URL |

---

## 8. Troubleshooting

### "ModuleNotFoundError" when running backend

Ensure the virtual environment is activated and dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

### Database connection refused

Verify PostgreSQL is running and the `DATABASE_URL` in `.env` is correct:
```bash
psql -U postgres -d hajj_pilgrims -c "SELECT 1;"
```

### Port 5432 already in use

Another PostgreSQL instance may be running. Either stop it or change the port mapping in the Docker Compose file.

### "Admin user already exists" on seed

This is expected if you have run the seed script before. The admin account is already in the database.

### CORS errors in browser console

Ensure `CORS_ORIGINS` in the backend `.env` includes `http://localhost:5173` and that the admin portal `.env` points to `http://localhost:8000/api/v1`.

### Audio cache not persisting in Docker

The Docker Compose configuration mounts `audio_cache_dev` as a named volume. If audio files disappear after container restart, verify the volume is present:
```bash
docker volume ls | grep audio
```
