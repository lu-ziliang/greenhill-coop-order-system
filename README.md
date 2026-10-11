markdown
README.md完整内容
# Greenhill Food Co-op Order System

A web-based ordering system for Greenhill Food Co-op's weekly grocery pickup.
Replaces paper order forms with an online ordering system supporting per-unit
and per-kilogram pricing.

## Features

- Member registration, login, and profile management
- Product management with per-unit and per-kilogram pricing
- Order round management (open / closed / packed states)
- Members place, edit, and cancel orders during open rounds
- Coordinator views all orders and product totals for wholesale purchasing
- Printable packing sheet organized by crate number with bay locations
- Correct pricing calculation with price locked at order time
- Automated tests for pricing logic

## Tech Stack

- Python / Flask (web framework)
- SQLite (database, via Flask-SQLAlchemy ORM)
- Jinja2 (templating)
- Flask-Login (authentication)
- pytest (testing)

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ziliang-lu/greenhill-coop-order-system.git
   cd greenhill-coop-order-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy environment template:
   ```
   cp .env.example .env          # macOS / Linux
   copy .env.example .env        # Windows
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

7. Open your browser to: http://127.0.0.1:5000

## Running Tests

```
pytest
```

## Branching Strategy

- `main`: Production-ready releases (tagged v1.0.0)
- `develop`: Integration branch
- `feature/GOS-XXX-description`: Feature branches for each Jira user story

## Configuration

All configuration is via environment variables in `.env` (template: `.env.example`):
- `DEBUG`: Set to True for development, False for production
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Test Accounts (illustrative only)

- Coordinator: username `coordinator`, password `demo123`
- Member: username `member1`, password `demo123`
