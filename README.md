# SLA Watchdog

![SLA Watchdog Logo](https://github.com/habert-kungu/watchdog/tree/main/tickets/templates/tickets/watchdog.png)

A Django-based ticket management system with SLA (Service Level Agreement) monitoring and email notifications. This application helps track ticket deadlines and automatically notifies users when tickets are approaching or have missed their SLA deadlines.

## Features

- **User Authentication**

  - Token-based authentication using Django REST Framework
  - User registration with email requirement
  - Secure login/logout functionality

- **Ticket Management**

  - Create, read, update, and delete tickets
  - Set deadlines for tickets
  - Track ticket status and SLA compliance
  - Email notifications for ticket creation

- **SLA Monitoring**

  - Automatic SLA violation detection
  - Warning notifications before SLA breach (1 hour before deadline)
  - Missed SLA notifications
  - Automated periodic checks via management command

- **Email Notifications**

  - Ticket creation confirmation
  - SLA warning alerts (1 hour before deadline)
  - SLA violation notifications
  - Configurable email settings via environment variables

- **Security**
  - CSRF protection
  - Token-based API authentication
  - Rate limiting for API endpoints

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd watchdog
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file in the project root with your email settings:

```env
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

## Usage

1. Start the development server:

```bash
python manage.py runserver
```

2. Access the dashboard at `http://localhost:8000/dashboard/`

3. Register a new user or login with existing credentials

4. Create tickets with:
   - Title
   - Description
   - Deadline

## API Endpoints

- `POST /register/`: Register new user
- `POST /api-token-auth/`: Obtain authentication token
- `GET /api/tickets/`: List all tickets
- `POST /api/tickets/`: Create new ticket
- `GET /api/tickets/{id}/`: Retrieve specific ticket
- `PUT /api/tickets/{id}/`: Update specific ticket
- `DELETE /api/tickets/{id}/`: Delete specific ticket

## SLA Monitoring

The system includes automated SLA monitoring with two types of notifications:

1. **Warning Notification**: Sent 1 hour before the deadline
2. **SLA Missed Notification**: Sent when a ticket passes its deadline

To enable automated SLA checking, set up a cron job to run the management command:

```bash
# Run every 15 minutes
*/15 * * * * /path/to/venv/bin/python /path/to/project/manage.py check_sla
```

## Email Configuration

Configure email settings in your `.env` file:

- `EMAIL_BACKEND`: Django email backend (default: smtp backend)
- `EMAIL_HOST`: SMTP server hostname
- `EMAIL_PORT`: SMTP port (usually 587 for TLS)
- `EMAIL_USE_TLS`: Whether to use TLS (True/False)
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `DEFAULT_FROM_EMAIL`: Default sender address

## Rate Limiting

The API includes rate limiting to prevent abuse:

- GET requests: 10 per minute per user
- POST requests: 5 per minute per user

## Development

### Running Tests

```bash
python manage.py test
```

### Check Code Style

```bash
flake8
black .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

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

## Email Configuration

This project sends emails for ticket creation and SLA notifications. For emails to function correctly, you must configure the following environment variables. These can be placed in a `.env` file in the project root directory.

- `EMAIL_BACKEND`: The Django email backend to use. Defaults to `django.core.mail.backends.smtp.EmailBackend`.
- `EMAIL_HOST`: The hostname or IP address of the SMTP server. (e.g., `smtp.example.com`)
- `EMAIL_PORT`: The port number for the SMTP server. (e.g., `587` for TLS, `25` for non-TLS)
- `EMAIL_USE_TLS`: Set to `True` if the SMTP server uses TLS, `False` otherwise.
- `EMAIL_HOST_USER`: The username for authenticating with the SMTP server.
- `EMAIL_HOST_PASSWORD`: The password for authenticating with the SMTP server.
- `DEFAULT_FROM_EMAIL`: The default email address to be used for outgoing emails (e.g., `noreply@yourdomain.com`). Ensure this address is authorized to send emails through your SMTP provider.

Example `.env` file content:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_mailtrap_username
EMAIL_HOST_PASSWORD=your_mailtrap_password
DEFAULT_FROM_EMAIL=noreply@example.com
```

## Running SLA Checks

The command `python manage.py check_sla` is available to check for ticket SLA warnings and misses. This command should be scheduled to run regularly (e.g., every 5-15 minutes) using a task scheduler like cron.

Example cron job (runs every 15 minutes):

```cron
*/15 * * * * /path/to/your/project/venv/bin/python /path/to/your/project/manage.py check_sla >> /path/to/your/project/logs/check_sla.log 2>&1
```

Make sure to replace `/path/to/your/project/` with the actual path to your project directory and adjust paths for your virtual environment and log file as needed.
