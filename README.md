# VPS Pilot

Multi-VPS server monitoring dashboard built with Django. Sign in as superadmin, view CPU / memory / disk usage across your local server and any remote VPS instances running VPS Pilot.

## Features

- **Superadmin-only login** — only Django superusers can access the dashboard
- **Sidebar layout** — clean admin UI with navigation
- **Server Info** — real-time gauges and progress bars for CPU, RAM, and disk
- **Multi-VPS** — add remote servers via Django admin; each VPS exposes a metrics API
- **PostgreSQL** — production-ready database configuration via environment variables

## Project structure

```
vpspilot/
├── .env.example          # Environment variable template
├── .gitignore
├── requirements.txt
├── README.md
└── config/
    ├── manage.py
    ├── config/           # Django project settings
    ├── accounts/         # Authentication (superadmin login)
    ├── servers/          # VPS registry, metrics collection, API
    ├── templates/        # HTML templates (Tailwind CSS)
    └── static/
```

## Quick start

### 1. Clone and set up environment

```bash
cd vpspilot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your SECRET_KEY, DB credentials, and METRICS_API_TOKEN
```

### 2. Create PostgreSQL database

```bash
sudo -u postgres psql -c "CREATE USER vpspilot WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "CREATE DATABASE vpspilot OWNER vpspilot;"
```

### 3. Run migrations and create superadmin

```bash
cd config
python manage.py migrate
python manage.py createsuperuser
python manage.py ensure_local_vps
```

### 4. Start the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) and sign in with your superadmin account.

## Adding remote VPS servers

1. Install VPS Pilot on the remote VPS (same steps as above).
2. Copy the remote server's `METRICS_API_TOKEN` from its `.env` file.
3. In your main installation, go to **Admin → VPS Servers → Add**.
4. Enter a name, the remote base URL (e.g. `https://vps2.example.com`), and the API token.
5. Open **Server Info** in the sidebar to see metrics from all servers.

The local server is registered automatically on first migration.

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (default: `localhost`) |
| `DB_PORT` | Database port (default: `5432`) |
| `METRICS_API_TOKEN` | Shared secret for the `/api/metrics/` endpoint |

## API

Remote installations poll each VPS via:

```
GET /api/metrics/
Header: X-API-Token: <METRICS_API_TOKEN>
```

Returns JSON with hostname, CPU %, memory, disk, load average, and uptime.

## Tech stack

- Django 6
- PostgreSQL
- Tailwind CSS (CDN)
- Chart.js (CDN) for usage gauges
- psutil for local system metrics
