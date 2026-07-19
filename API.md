# Hajj Pilgrims Management API Documentation

## Overview

Privacy-preserving AI-based multimodal mobile information delivery system for Hajj pilgrims. This backend powers a React admin portal and a Flutter mobile app (not yet built).

**Base URL:** `http://localhost:8000/api/v1`

**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI) | `http://localhost:8000/redoc` (ReDoc)

---

## Authentication

All protected endpoints require a **JWT Bearer token** in the `Authorization` header.

```
Authorization: Bearer <access_token>
```

**Token flow:**

1. `POST /auth/login` with email and password to receive an `access_token` and `refresh_token` pair.
2. Use the `access_token` for all authenticated requests.
3. When the access token expires (30 minutes), call `POST /auth/refresh` with the `refresh_token` to get a new pair (rotation).
4. `POST /auth/logout` revokes the refresh token.

**Default admin credentials:**
- Email: `admin@hajj.ng`
- Password: `admin123`

**Roles:**
- `admin` -- Full access to all endpoints (React admin portal only).
- `pilgrim` -- Limited access to own data, announcements, notifications, and AI queries (Flutter app).

---

## Response Format

All API responses follow a standardized envelope:

```json
{
  "success": true,
  "message": "Pilgrims retrieved successfully",
  "data": { ... },
  "errors": null
}
```

**Success response fields:**

| Field     | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| `success` | `bool`  | `true` for successful requests.                  |
| `message` | `str`   | Human-readable description of the result.         |
| `data`    | `any`   | The response payload (object, array, or `null`). |
| `errors`  | `any`   | Validation or business logic errors, or `null`.   |

**Error response example (422 Validation Error):**

```json
{
  "success": false,
  "message": "Validation error",
  "data": null,
  "errors": [
    {"field": "body -> email", "message": "field required"},
    {"field": "body -> password", "message": "String should have at least 8 characters"}
  ]
}
```

**Paginated responses** include a `data` object with these fields:

```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "size": 20,
  "pages": 8
}
```

---

## Endpoint Groups

### Auth

Authentication, registration, and token management.

| Method | Path            | Description                       | Auth Required |
|--------|-----------------|-----------------------------------|---------------|
| POST   | `/auth/register` | Register a new pilgrim account   | No            |
| POST   | `/auth/login`    | Login and receive tokens         | No            |
| POST   | `/auth/refresh`  | Refresh access token (rotation)  | No            |
| POST   | `/auth/logout`   | Revoke refresh token             | Yes           |
| GET    | `/auth/me`       | Get current user profile         | Yes           |

**Rate limits:** Register: 5/min, Login: 10/min.

---

### Pilgrims

CRUD operations for pilgrim management. Admin only.

| Method | Path                  | Description                              | Auth Required |
|--------|-----------------------|------------------------------------------|---------------|
| GET    | `/pilgrims`           | List pilgrims (paginated, searchable)    | Admin         |
| GET    | `/pilgrims/{id}`      | Get pilgrim by ID                        | Admin         |
| POST   | `/pilgrims`           | Create a new pilgrim                     | Admin         |
| PUT    | `/pilgrims/{id}`      | Update pilgrim profile                   | Admin         |
| DELETE | `/pilgrims/{id}`      | Delete pilgrim (cascade)                 | Admin         |

**Query parameters (list):** `search` (name/email/phone/nationality/passport), `package_id` (filter by package), `page`, `size`, `sort_by`, `sort_order`.

---

### Flights

Flight booking management with status tracking. Admin only.

| Method | Path               | Description                                | Auth Required |
|--------|--------------------|--------------------------------------------|---------------|
| GET    | `/flights`         | List flights (paginated, searchable)       | Admin         |
| GET    | `/flights/{id}`    | Get flight by ID                           | Admin         |
| POST   | `/flights`         | Create a new flight                        | Admin         |
| PUT    | `/flights/{id}`    | Update flight details                      | Admin         |
| DELETE | `/flights/{id}`    | Delete flight                              | Admin         |

**Query parameters (list):** `search` (airline/flight number/airports), `status` (pending/in_progress/completed), `page`, `size`, `sort_by`, `sort_order`.

**Status values:** `pending`, `in_progress`, `completed`.

---

### Accommodations

Hotel and accommodation management. Admin only.

| Method | Path                      | Description                                | Auth Required |
|--------|---------------------------|--------------------------------------------|---------------|
| GET    | `/accommodations`         | List accommodations (paginated)            | Admin         |
| GET    | `/accommodations/{id}`    | Get accommodation by ID                    | Admin         |
| POST   | `/accommodations`         | Create a new accommodation                 | Admin         |
| PUT    | `/accommodations/{id}`    | Update accommodation details               | Admin         |
| DELETE | `/accommodations/{id}`    | Delete accommodation                       | Admin         |

**Query parameters (list):** `search` (hotel/city/room), `city` (partial match filter), `page`, `size`, `sort_by`, `sort_order`.

---

### Transports

Ground transportation management. Admin only.

| Method | Path                   | Description                                | Auth Required |
|--------|------------------------|--------------------------------------------|---------------|
| GET    | `/transports`          | List transports (paginated)                | Admin         |
| GET    | `/transports/{id}`     | Get transport by ID                        | Admin         |
| POST   | `/transports`          | Create a new transport assignment          | Admin         |
| PUT    | `/transports/{id}`     | Update transport details                   | Admin         |
| DELETE | `/transports/{id}`     | Delete transport                           | Admin         |

**Query parameters (list):** `search` (vehicle number/locations/driver), `type` (transport type filter), `page`, `size`, `sort_by`, `sort_order`.

---

### Packages

Hajj package management with component linking and pilgrim assignment. Admin only.

| Method | Path                                   | Description                              | Auth Required |
|--------|----------------------------------------|------------------------------------------|---------------|
| GET    | `/packages`                            | List packages (paginated)                | Admin         |
| GET    | `/packages/{id}`                       | Get package with full details            | Admin         |
| POST   | `/packages`                            | Create a new package                     | Admin         |
| PUT    | `/packages/{id}`                       | Update package details                   | Admin         |
| DELETE | `/packages/{id}`                       | Delete package (unlinks pilgrims)        | Admin         |
| POST   | `/packages/{id}/assign/{pilgrim_id}`   | Assign package to pilgrim                | Admin         |
| GET    | `/packages/{id}/pilgrims`              | List pilgrims in a package (paginated)   | Admin         |

**Package components:** Each package links to a `flight_id`, `accommodation_id`, and `transport_id`. All references are validated on create/update.

---

### Announcements

Announcement templates with placeholders, active announcements, and pilgrim-scoped personalization.

| Method | Path                                  | Description                              | Auth Required |
|--------|---------------------------------------|------------------------------------------|---------------|
| GET    | `/announcements`                      | List all announcement templates (admin)  | Admin         |
| GET    | `/announcements/my`                   | Get personalized announcements (pilgrim) | Pilgrim       |
| GET    | `/announcements/active`               | Get currently active announcements       | No            |
| GET    | `/announcements/templates/placeholders` | List available template placeholders   | No            |
| GET    | `/announcements/{id}`                 | Get announcement by ID                   | Admin         |
| POST   | `/announcements`                      | Create announcement template             | Admin         |
| PUT    | `/announcements/{id}`                 | Update announcement template             | Admin         |
| DELETE | `/announcements/{id}`                 | Delete announcement template             | Admin         |

**Target types:** `all`, `pilgrim`, `package`, `flight`, `accommodation`, `transport`.

**Placeholders:** `{{pilgrim_name}}`, `{{flight_number}}`, `{{departure_time}}`, `{{departure_airport}}`, `{{arrival_airport}}`, `{{hotel_name}}`, `{{room_number}}`, `{{city}}`, `{{bus_number}}`, `{{pickup_location}}`, `{{destination}}`, `{{pickup_time}}`, and more. Use `GET /announcements/templates/placeholders` for the full list.

**Query parameters (list):** `search` (title/message), `priority` (low/medium/high/urgent), `target_type`, `page`, `size`, `sort_by`, `sort_order`.

---

### Preferences

CRUD for pilgrim display and notification preferences. Admin only.

| Method | Path                         | Description                              | Auth Required |
|--------|------------------------------|------------------------------------------|---------------|
| GET    | `/preferences`               | List all preferences (paginated)         | Admin         |
| GET    | `/preferences/{id}`          | Get preference by ID                     | Admin         |
| GET    | `/preferences/by-pilgrim/{id}` | Get preference by pilgrim ID           | Admin         |
| POST   | `/preferences`               | Create preference for a pilgrim          | Admin         |
| PUT    | `/preferences/{id}`          | Update preference                        | Admin         |
| DELETE | `/preferences/{id}`          | Delete preference                        | Admin         |

**Preference fields:** `preferred_language`, `delivery_mode`, `font_size` (8-48), `notifications_enabled`.

**Query parameters (list):** `search` (pilgrim name/email), `pilgrim_id`, `language`, `delivery_mode`, `page`, `size`, `sort_by`, `sort_order`.

---

### Notifications

System-generated notifications for pilgrims based on package data. Device token registration for push notifications.

| Method | Path                          | Description                              | Auth Required |
|--------|-------------------------------|------------------------------------------|---------------|
| GET    | `/notifications`              | List all notifications (admin)           | Admin         |
| GET    | `/notifications/my`           | Get my notifications (pilgrim)           | Pilgrim       |
| PATCH  | `/notifications/{id}/read`    | Mark notification as read                | Yes (owner or admin) |
| POST   | `/notifications/devices`      | Register FCM/APNs device token           | Yes           |
| DELETE | `/notifications/devices/{id}` | Deactivate device token                  | Pilgrim       |

**Notification types:** `flight`, `accommodation`, `transport`, `announcement`, `reminder`, `general`.

**Notification statuses:** `pending`, `sent`, `delivered`, `read`, `failed`.

**Query parameters (list):** `type`, `status`, `pilgrim_id`, `page`, `size`, `sort_by`, `sort_order`.

---

### AI Personalization

AI-powered content simplification and translation using Google Gemini. The `/ask` and `/ask/audio` endpoints are pilgrim-scoped (the AI only sees that pilgrim's own data). Admin endpoints process arbitrary text.

| Method | Path                  | Description                              | Auth Required |
|--------|-----------------------|------------------------------------------|---------------|
| POST   | `/personalize/ask`    | Ask a question about your Hajj data      | Pilgrim       |
| POST   | `/personalize/ask/audio` | Ask and receive audio response         | Pilgrim       |
| POST   | `/personalize/simplify` | Simplify announcement text (plain language) | Admin     |
| POST   | `/personalize/translate` | Translate text between languages       | Admin         |
| POST   | `/personalize/process` | Full processing pipeline (simplify + translate + audio) | Admin |
| GET    | `/personalize/health` | Check AI provider status                 | Admin         |

**Rate limits:** Ask: 20/min, Ask+Audio: 10/min.

**Supported languages:** English, Hausa, Arabic, Yoruba, Igbo.

---

### Text-to-Speech (TTS)

Convert text to audio in multiple languages with caching.

| Method | Path                  | Description                              | Auth Required |
|--------|-----------------------|------------------------------------------|---------------|
| POST   | `/tts`                | Convert text to speech (MP3)             | Admin         |
| GET    | `/tts/audio/{file}`   | Download cached audio file               | No            |

**Rate limits:** 10/min.

**Cache:** Audio files are cached by `sha256(text + language_code)`. Subsequent requests for the same text+language return the cached file.

---

### Health & Stats

Service health check and dashboard statistics.

| Method | Path      | Description                              | Auth Required |
|--------|-----------|------------------------------------------|---------------|
| GET    | `/health` | Service health check                     | No            |
| GET    | `/stats`  | Dashboard statistics (aggregate counts)  | Admin         |

**Stats response fields:** `total_pilgrims`, `active_pilgrims`, `total_packages`, `total_flights`, `total_accommodations`, `total_transports`, `total_announcements`, `total_notifications`, `total_preferences`.

---

## Rate Limits

Rate limiting is applied per IP address using SlowAPI.

| Endpoint            | Limit       |
|---------------------|-------------|
| `POST /auth/register` | 5/min     |
| `POST /auth/login`    | 10/min    |
| `POST /personalize/ask` | 20/min  |
| `POST /personalize/ask/audio` | 10/min |
| `POST /tts`            | 10/min   |

Rate limit exceeded returns HTTP 429:
```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later.",
  "data": null,
  "errors": null
}
```

---

## Error Codes

| HTTP Code | Description                                      |
|-----------|--------------------------------------------------|
| 200       | Success                                          |
| 201       | Created successfully                             |
| 204       | Deleted successfully (no content returned)       |
| 400       | Bad request (e.g., duplicate email, invalid dates) |
| 401       | Invalid credentials or missing/expired token     |
| 403       | Insufficient permissions (wrong role)            |
| 404       | Resource not found                               |
| 409       | Database constraint violation                    |
| 422       | Validation error (missing/invalid fields)        |
| 429       | Rate limit exceeded                              |
| 500       | Internal server error                            |
| 502       | AI provider error (Gemini API failure)           |
| 503       | Service unavailable (AI not configured)          |

---

## Pagination Parameters

All list endpoints support these query parameters:

| Parameter   | Default | Description                          |
|-------------|---------|--------------------------------------|
| `page`      | 1       | Page number (1-indexed)              |
| `size`      | 20      | Items per page                       |
| `sort_by`   | `id`    | Field to sort by                     |
| `sort_order`| `asc`   | Sort direction: `asc` or `desc`      |
| `search`    | `""`    | Free-text search across name fields  |
