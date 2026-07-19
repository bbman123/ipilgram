# Privacy-Preserving AI-Based Multimodal Mobile Information Delivery System for Hajj Pilgrims in Nigeria

An MSc research project implementing an intelligent information delivery platform for Hajj pilgrims. The system provides personalized travel information, AI-powered content simplification and translation, multi-language text-to-speech, and real-time push notifications -- all with a strong emphasis on data privacy and security.

## Overview

The Hajj pilgrimage is one of the largest annual gatherings in the world, with millions of pilgrims traveling to Saudi Arabia. Nigerian pilgrims face unique challenges including language barriers, limited access to real-time travel information, and the complexity of coordinating flights, accommodation, and transportation. This system addresses these challenges through a privacy-preserving AI-powered platform that delivers personalized multimodal information directly to pilgrims.

The platform consists of three components:
- A **FastAPI backend** serving as the core API with 65 endpoints
- A **React admin portal** for administrators to manage pilgrims, packages, announcements, and system operations
- A **Flutter mobile app** (in development) for pilgrims to receive personalized information on their devices

**Important**: The React admin portal is strictly for administrative use. Pilgrims do not interact with the React application -- they will use the Flutter mobile app exclusively.

## Key Features

- **Pilgrim Management** -- Full CRUD operations with search, filtering, sorting, and pagination. Pilgrims are assigned packages containing flight, accommodation, and transport components.
- **Package Management** -- Hajj packages linking flights, accommodations, and ground transport with aggregate pricing and pilgrim assignment.
- **Announcement System** -- Templated announcements with placeholder substitution (e.g., `{{pilgrim_name}}`, `{{flight_number}}`), targeted delivery by pilgrim, package, flight, accommodation, or transport.
- **AI Personalization** -- Google Gemini integration for content simplification, translation, and a full personalization pipeline.
- **Multi-Language TTS** -- gTTS-based text-to-speech supporting English, Hausa, Arabic, Yoruba, and Igbo with audio file caching.
- **Push Notifications** -- Firebase Cloud Messaging (FCM) with device token management and background notification engine.
- **JWT Authentication** -- Access/refresh token rotation with BCrypt-hashed refresh tokens stored in the database.
- **Rate Limiting** -- Per-endpoint rate limits using SlowAPI.
- **Security Headers** -- Custom middleware adding XSS protection, CSP, HSTS, frame denial, and other security headers.
- **Standardized API Responses** -- Consistent `{success, message, data, errors}` envelope across all endpoints.
- **Background Scheduler** -- APScheduler running a notification engine every 5 minutes.
- **Health Checks** -- Built-in health endpoint for monitoring and deployment readiness probes.

## Tech Stack

### Backend

| Component | Technology |
|---|---|
| Framework | FastAPI 0.115 |
| Language | Python 3.11 |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL 18 |
| Migrations | Alembic |
| Authentication | python-jose, bcrypt |
| Rate Limiting | SlowAPI |
| Scheduler | APScheduler |
| TTS | gTTS |
| AI | Google Gemini |
| Push Notifications | Firebase Admin SDK |
| Production Server | Gunicorn + Uvicorn workers |

### Frontend (Admin Portal)

| Component | Technology |
|---|---|
| Framework | React 19 |
| Language | TypeScript 6.0 |
| Build Tool | Vite 8.1 |
| Styling | TailwindCSS 4.3 |
| HTTP Client | Axios |
| Routing | React Router DOM 7 |
| Linting | oxlint |

### Mobile (In Development)

| Component | Technology |
|---|---|
| Framework | Flutter |
| Target | Android and iOS |

### DevOps

| Component | Technology |
|---|---|
| Containers | Docker, Docker Compose |
| Deployment | Render (backend + PostgreSQL) |
| CI/CD | Render auto-deploy from repository |

## Architecture

```
                          +-------------------+
                          |   Flutter Mobile   |
                          |     (Pilgrims)     |
                          +---------+---------+
                                    |
                                    | HTTPS
                                    v
+---------------+         +-------------------+         +-------------------+
|  React Admin  |  ---->  |   FastAPI Backend  |  ---->  |    PostgreSQL      |
|  Portal       |  HTTPS  |   (Port 8000)     |  SQLAlchemy  |    Database       |
|  (Admins)     |         |                   |         +-------------------+
+---------------+         +-------------------+
                                    |
                          +---------+---------+
                          |                   |
                          v                   v
                 +----------------+  +------------------+
                 | Google Gemini  |  | Firebase (FCM)   |
                 | (AI Services)  |  | (Push Notifs)    |
                 +----------------+  +------------------+
                          |
                          v
                 +----------------+
                 | gTTS Engine    |
                 | (Audio Cache)  |
                 +----------------+
```

### Data Flow

1. **Admins** authenticate via the React portal and manage pilgrims, packages, flights, accommodations, transports, and announcements.
2. **Announcements** use template placeholders that are resolved per-pilgrim based on their assigned package data.
3. **AI Services** simplify and translate announcement content for individual pilgrims based on their language preferences.
4. **TTS Engine** converts personalized text to audio in the pilgrim's preferred language.
5. **Notification Engine** (APScheduler) processes pending notifications and dispatches them via FCM.
6. **Pilgrims** receive personalized, multi-language information through the mobile app.

## API Documentation

The backend exposes 65 API endpoints across 13 resource groups:

| Group | Endpoints | Description |
|---|---|---|
| Health | 1 | Service health check |
| Dashboard | 1 | Statistics and analytics |
| Auth | 4 | Registration, login, token refresh, logout, profile |
| Pilgrims | 5 | CRUD with search, filtering, pagination |
| Flights | 5 | Flight management with status tracking |
| Accommodations | 5 | Hotel and accommodation management |
| Transports | 5 | Ground transportation management |
| Packages | 5 | Hajj package management with component linking |
| Announcements | 7 | Templates with placeholders and targeted delivery |
| Preferences | 5 | Display and notification preferences |
| AI Personalization | 3 | Simplify, translate, full pipeline |
| Text-to-Speech | 2 | Multi-language audio generation |
| Notifications | 3 | System notifications and device token management |

Interactive documentation is available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Project Structure

```
ipilgram/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # Route handlers (13 modules)
│   │   ├── core/             # Config, database, security, rate limiting
│   │   ├── models/           # SQLAlchemy models (10 tables)
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic (AI, TTS, FCM, notifications)
│   │   ├── middleware.py      # Security headers, request ID
│   │   └── main.py           # FastAPI application factory
│   ├── alembic/              # Database migration scripts
│   ├── tests/                # Test suite
│   ├── seed.py               # Admin user seeding
│   ├── Dockerfile            # Multi-stage Docker build
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variable template
├── admin-portal/
│   ├── src/                  # React components and pages
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   └── .env.example          # Frontend environment template
├── mobile/                   # Flutter app (in development)
├── docs/                     # Additional documentation
├── docker-compose.yml        # Development Docker Compose
├── docker-compose.prod.yml   # Production Docker Compose
├── render.yaml               # Render deployment config
└── README.md                 # This file
```

## Quick Start

See [INSTALL.md](INSTALL.md) for detailed setup instructions.

```bash
# Clone the repository
git clone https://github.com/your-username/ipilgram.git
cd ipilgram

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Edit with your values
alembic upgrade head
python seed.py
uvicorn app.main:app --reload

# Frontend setup (separate terminal)
cd admin-portal
npm install
cp .env.example .env
npm run dev
```

Admin login: `admin@hajj.ng` / `admin123`

## Deployment

The project is configured for deployment on Render using the included `render.yaml` blueprint. The backend runs as a Gunicorn web service with Uvicorn workers, connected to a managed PostgreSQL instance. Audio files are stored on a persistent disk mount.

For Docker-based deployment:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

## Security Considerations

- Refresh tokens are stored as BCrypt hashes in the database, never in plaintext.
- Token rotation ensures old refresh tokens are revoked on each use.
- Rate limiting prevents brute-force attacks on authentication endpoints.
- Security headers (CSP, HSTS, X-Frame-Options, etc.) are applied to all responses.
- TrustedHosts middleware restricts allowed hostnames in production.
- The `SECRET_KEY` validator warns against weak or default keys.
- All API responses use a standardized envelope to prevent information leakage.

## License

This project is part of an MSc research submission. All rights reserved.

## Contact

For questions about this research project, please contact the research team.
