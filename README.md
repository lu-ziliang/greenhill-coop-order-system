# Greenhill Food Co-op Ordering System

ISYS3001 A3 Project - Greenhill Food Co-op Web Application

## Project Description

This is a web application developed for Greenhill Food Co-op to manage member orders, product listings, and packing sheets. The system allows members to browse products, place orders during active rounds, and track their order history. Coordinators can manage products, view all orders, generate packing sheets, and create new order rounds.

## Team Members

- Ziliang Lu (25259146) - Backend Development, User Authentication
- Puhao Guo - Product Management, Documentation
- Yaohan Jia - Testing, Jira Management, Packing Features

## Technologies Used

- Backend: Python Flask Framework
- Database: SQLite with SQLAlchemy ORM
- Authentication: Flask-Login
- Frontend: HTML/CSS with Bootstrap
- Version Control: Git/GitHub
- Project Management: Jira + Confluence
- Testing: pytest

## Project Structure

```
greenhill-coop-order-system/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main pages
│   │   ├── products.py      # Product management
│   │   ├── orders.py        # Order management
│   │   └── rounds.py        # Round management
│   └── templates/           # HTML templates
├── tests/                   # Automated tests
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # This file
```

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lu-ziliang/greenhill-coop-order-system.git
   cd greenhill-coop-order-system
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

## Features Implemented

### User Authentication
- Member registration with email verification
- Secure login/logout with password hashing
- Member profile management

### Product Management
- Browse products (for members)
- Add/edit/delete products (for coordinators)
- Product pricing: per-unit or per-kg
- Product withdrawal/deactivation

### Order Management
- Place orders during active rounds
- Edit/cancel orders before round closes
- View personal order history
- Real-time order total calculation

### Coordinator Tools
- View all orders in current round
- Product totals summary for wholesale purchasing
- Create/manage order rounds (open/closed/packed)
- Generate printable packing sheets

### Packing
- Packing sheet grouped by member
- Record actual packed quantities
- Download/print packing list

## Project Management Links

- Jira Board: https://scu-it.atlassian.net/jira/software/c/projects/MSD426GXUST29/boards/2021
- Confluence Space: https://scu-it.atlassian.net/wiki/spaces/MSD426GXUST29

## Sprint Status

- Total User Stories: 14
- Completed: 14 (100%)
- Test Cases Passed: 14/14

## Acknowledgments

- ISYS3001 Course Team
- Greenhill Food Co-op (Sample Project)
- Southern Cross University
































































































