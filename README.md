# PulseFit — Fitness & Wellness Web Application

A full-stack fitness tracking and wellness management web application powered by **Python (Django)** and responsive HTML templates.

## Key Features
- **Program & Workout Showcase:** Structured views for fitness routines, membership plans, or wellness tracking.
- **Dynamic Templates:** Server-rendered pages powered by Django's template engine.
- **Database Integration:** Persistent storage for user or activity records via Django ORM.

## Technologies Used
- **Python & Django** — Backend application logic, views, and URL routing.
- **HTML5 & CSS3** — Responsive front-end templates and user interface styling.
- **SQLite** — Default relational database.

## How to Run Locally
1. Clone the repository and enter the project directory:
   ```bash
   git clone https://github.com
   cd pulsefit-django-app
   ```
2. Install dependencies and run migrations:
   ```bash
   pip install django
   python manage.py migrate
   ```
3. Launch the local server:
   ```bash
   python manage.py runserver
   ```
4. Visit `http://127.0.0.1:8000` in your web browser.
