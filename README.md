# Greenhill Food Co-op Ordering System

A web-based ordering system for Greenhill Food Co-op, built with Flask.

## Features

- Member registration and authentication
- Product catalog management
- Order placement and management
- Order round coordination
- Packing sheet generation
- Role-based access (member / coordinator)

## Tech Stack

- Python 3.10+
- Flask 3.0
- Flask-SQLAlchemy
- Flask-Login
- SQLite (development)
- Jinja2 templates

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run the application: `python run.py`
7. Open http://127.0.0.1:5000

## Project Structure

```
greenhill-coop-order-system/
├── app/
│   ├── __init__.py       # Application factory
│   ├── models.py          # Database models
│   ├── routes/            # Blueprint routes
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   └── rounds.py
│   └── templates/         # Jinja2 HTML templates
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── CHANGELOG.md           # Change log
```

## Branching Strategy

This project uses Git Flow:
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches

## License

This project is for educational purposes as part of ISYS3001 Managing Software Development.
