# Scalable URL Shortener

A **production-style URL shortener backend** built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**.
This project demonstrates backend engineering concepts such as **rate limiting, caching, analytics tracking, and containerized deployment**.

---

## Features

* Shorten long URLs into compact shareable links
* Redirect users using short codes
* Click analytics tracking
* Rate limiting using Redis
* PostgreSQL database storage
* Dockerized deployment
* Clean modular backend architecture

---

## Tech Stack

* **FastAPI** – backend API
* **PostgreSQL** – relational database
* **Redis** – caching and rate limiting
* **SQLAlchemy** – ORM
* **SlowAPI** – rate limiting
* **Jinja2** – templating
* **Docker & Docker Compose** – containerized environment

---

## Architecture

Client → FastAPI → Redis → PostgreSQL

* **FastAPI** handles API requests
* **Redis** handles rate limiting and caching
* **PostgreSQL** stores URLs and click analytics

---

## Project Structure

```
UrlShortner
│
├── core/               # configuration and settings
├── database/           # database session and models
├── routers/            # API route handlers
├── services/           # business logic
├── schemas/            # request/response schemas
├── templates/          # HTML templates
├── static/             # static files (CSS, JS)
│
├── main.py             # FastAPI entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Running the Project

### Using Docker (Recommended)

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost:8000
```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```
DATABASE_URL=postgresql+psycopg2://postgres:password@postgres:5432/urlshortnerdatabase
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
```

---

## API Endpoints

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | /                 | Homepage                 |
| POST   | /generate         | Create short URL         |
| GET    | /{code}         | Redirect to original URL |
| GET    | /health           | Health check             |
| GET    | /analytics/{code} | View analytics           |

---

## Example Flow

1. User submits a long URL
2. Backend generates a short code
3. URL stored in PostgreSQL
4. User accesses the short link
5. Click analytics recorded
6. Redis enforces rate limiting

---

## License

This project is open-source and available for learning purposes.
