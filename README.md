# SLA Watchdog

A tiny Django REST API that tracks ticket deadlines and notifies users when a ticket is about to, or has already, missed its SLA.

## Features

- Token-based authentication (DRF Token Auth)
- Ticket CRUD API
- Rate limiting (django-ratelimit)
- Email notifications for SLA warnings and misses

## Setup

### 1. Clone and Install Dependencies

```
conda activate <your-env>
pip install django djangorestframework djangorestframework-simplejwt django-ratelimit
```

### 2. Database Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```
python manage.py createsuperuser
```

### 4. Configure Email

Edit `watchdog/settings.py`:

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '<your-smtp-server>'
EMAIL_PORT = 587  # or 465/25 as needed
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '<your-email>'
EMAIL_HOST_PASSWORD = '<your-password>'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

### 5. Run the Server

```
python manage.py runserver
```

## API Usage

### Authentication

- Obtain a token:
  - `POST /api-token-auth/` with `{ "username": "<user>", "password": "<pass>" }`
  - Use `Authorization: Token <token>` header for all requests.

### Endpoints

- `GET /api/tickets/` — List tickets (rate limited: 10/min)
- `POST /api/tickets/` — Create ticket (rate limited: 5/min)
- `GET /api/tickets/<id>/` — Retrieve ticket
- `PUT/PATCH/DELETE /api/tickets/<id>/` — Update/delete ticket

## SLA Notification Logic

- Each ticket has a deadline.
- If a ticket is within 1 hour of missing its SLA, a warning email is sent.
- If a ticket misses its SLA, a missed notification email is sent.

## Automating SLA Checks

To automate SLA checks and notifications, add a periodic task (e.g., via cron or Celery) to run:

```
from tickets.models import Ticket
for ticket in Ticket.objects.all():
    ticket.check_and_notify_sla()
```

Or create a Django management command for this purpose.

## Rate Limiting

- GET /api/tickets/: 10 requests per minute per user
- POST /api/tickets/: 5 requests per minute per user

## License

MIT
