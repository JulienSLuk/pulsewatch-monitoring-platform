# PulseWatch Monitoring Platform

PulseWatch is a lightweight service monitoring system that tracks uptime, response time, and service health.

## Features

- API-based service monitoring
- Background monitoring worker
- Live dashboard
- Response time tracking
- Automatic failure detection

## Tech Stack

- Python
- FastAPI
- SQLite
- APScheduler
- HTML / JavaScript dashboard

## Running the Project

Install dependencies:

```
pip install -r requirements.txt
```

Start the server:

```
python -m uvicorn app.main:app --reload
```

Open dashboard:

```
http://127.0.0.1:8000
```

## Example API

Add a monitored service:

```
POST /services
```

```json
{
"name": "Example",
"url": "https://example.com"
}
```

## Dashboard

Shows service status and response time.

## Future Improvements

- authentication
- multi-user monitoring
- uptime analytics
- alerting system
