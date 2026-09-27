# ⏱️ TimeTrack — Habit Tracker with Analytics

A modern, full-stack habit tracking and analytics web application designed to help users establish consistency, track daily habits, visualize progress over time, and gain data-driven insights into their personal routines.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-ECS%20Fargate-FF9900?logo=amazonaws&logoColor=white)

> 🚧 **This project is actively under development.** Core architecture and requirements are defined; backend, frontend, and AWS deployment are being built out incrementally. See the [Roadmap](#-roadmap) below for current progress.

---

## ✨ Features

- 📌 Create and manage daily, weekly, or custom-frequency habits
- ✅ Log completions and automatically calculate current & longest streaks
- 📊 Analytics dashboard with completion-rate charts over 7-day, 30-day, and all-time windows
- 🔐 Secure JWT-based authentication
- 🐳 Fully containerized for consistent local development and cloud deployment
- ☁️ Deployable to AWS via ECS Fargate with zero server management

---

## 🗺️ Roadmap

- [x] Requirements analysis & system design
- [ ] Backend API (FastAPI + PostgreSQL + JWT auth)
- [ ] Frontend UI (Next.js + Tailwind + Recharts dashboard)
- [ ] Dockerize backend & frontend
- [ ] Local Docker Compose environment
- [ ] Deploy to AWS (ECS Fargate + RDS)
- [ ] CI/CD pipeline

---

## 🛠 Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+), SQLAlchemy (async), Alembic, Pydantic v2
- **Frontend:** [Next.js](https://nextjs.org/) (App Router / TypeScript), Tailwind CSS, Lucide Icons, Recharts
- **Database:** [PostgreSQL 16](https://www.postgresql.org/) with `asyncpg`
- **Containerization & Orchestration:** [Docker](https://www.docker.com/) & Docker Compose
- **Cloud:** AWS ECS Fargate, RDS, Secrets Manager, CloudFront + S3

---

## 📋 Prerequisites

Before running the project locally, ensure you have the following installed:

- **Docker & Docker Compose** (Docker Desktop on Windows / macOS / Linux)
- **Node.js**: v20+ (for local frontend development)
- **Python**: v3.12+ (for local backend development)
- **Git**

---

## 🚀 Quick Start (Docker Compose)

The easiest way to get TimeTrack running is using Docker Compose:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jamir-Lagua/timetrack.git
   cd timetrack
   ```

2. **Copy the example environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Build and spin up the full stack:**
   ```bash
   docker-compose up --build -d
   ```
   *(Or run `make up`)*

4. **Verify the services:**
   - **Frontend:** [http://localhost:3000](http://localhost:3000)
   - **Backend API:** [http://localhost:8000](http://localhost:8000)
   - **API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **PostgreSQL Database:** `localhost:5432`

5. **Stop all services:**
   ```bash
   docker-compose down
   ```
   *(Or run `make down`)*

---

## 💻 Local Development

If you prefer running services without Docker containers for hot reloading and faster iteration:

### 1. Database Setup
Start only the PostgreSQL container:
```bash
docker-compose up -d db
```

### 2. Backend Setup (FastAPI)
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Start Next.js development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📖 API Documentation

FastAPI provides interactive API documentation out of the box:
- **Interactive Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema (JSON):** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 📂 Project Structure

```
TimeTrack/
├── backend/
│   ├── alembic/              # Database migration scripts
│   ├── app/
│   │   ├── api/              # API route controllers
│   │   ├── core/             # Configuration, security, database session
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Business logic and habit analytics
│   │   └── main.py           # Application entrypoint
│   ├── tests/                # Pytest test suite
│   ├── Dockerfile            # Production backend Docker image
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── app/              # Next.js App Router pages and layouts
│   │   ├── components/       # Reusable UI components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utility functions and API client
│   │   └── types/            # TypeScript type definitions
│   ├── Dockerfile            # Multi-stage production frontend Docker image
│   ├── package.json          # Node dependencies & scripts
│   └── tailwind.config.ts    # Tailwind styling configuration
├── .env.example              # Sample environment variables
├── .gitignore                # Git ignore rules
├── docker-compose.yml        # Multi-container Docker orchestration
├── Makefile                  # Helper commands for local management
└── README.md                 # Project documentation
```

---

## ⚙️ Environment Variables

The following environment variables configure the system:

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://timetrack:timetrack_dev@db:5432/timetrack` |
| `SECRET_KEY` | Secret key for JWT signing & authentication | `change-this-to-a-random-secret-key` |
| `ACCESS_TOKEN_EXPIRE_DAYS` | Expiration time for JWT access tokens | `7` |
| `CORS_ORIGINS` | Comma-separated list of allowed CORS origins | `http://localhost:3000` |
| `NEXT_PUBLIC_API_URL` | Backend API URL accessible from the client | `http://localhost:8000` |

---

## ☁️ Deployment

For production cloud deployments, the recommended architecture is:

- **Compute:** **AWS ECS Fargate**
  - Run containerized backend and frontend services as serverless tasks within an Amazon ECS cluster behind an **Application Load Balancer (ALB)**.
  - Autoscaling enabled based on CPU/Memory metrics.
- **Database:** **AWS RDS for PostgreSQL**
  - Multi-AZ deployment for high availability.
  - Automated backups, encryption at rest via AWS KMS, and connection pooling.
- **Secrets Management:** **AWS Secrets Manager** / **SSM Parameter Store** for storing `SECRET_KEY` and database credentials.
- **Static Assets & CDN:** **Amazon CloudFront** + **S3** (or Next.js standalone server on ECS) for low-latency asset delivery.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).