# Smart Job Tracker

A web-based job application tracking system built with **Django** that helps users organize, manage, and track their job applications in one place.

## 🚀 Live Demo

**Live Application:**
https://smart-job-tracker-hu0d.onrender.com

## 📌 Features

* User registration and login
* Secure user authentication
* Add new job applications
* Edit existing job applications
* Delete job applications
* View job details
* Track application status
* Track application deadlines
* Maintain application status history
* User-specific job data
* Responsive web interface
* PostgreSQL database for production
* Static file handling with WhiteNoise
* Production deployment using Gunicorn and Render

## 🛠️ Tech Stack

### Backend

* Python
* Django
* Django ORM
* Django Authentication

### Frontend

* HTML
* CSS
* Bootstrap
* Django Templates

### Database

* SQLite for local development
* PostgreSQL for production

### Deployment & Tools

* Git
* GitHub
* Gunicorn
* WhiteNoise
* Render

## 📂 Project Structure

```text
smart-job-tracker/
│
├── jobs/
│   ├── migrations/
│   ├── templates/
│   │   └── jobs/
│   │       ├── add_job.html
│   │       ├── base.html
│   │       ├── delete_job.html
│   │       ├── edit_job.html
│   │       ├── home.html
│   │       ├── job_detail.html
│   │       ├── job_list.html
│   │       ├── login.html
│   │       └── register.html
│   │
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── smart_job_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mdnawaz78/smart-job-tracker.git
cd smart-job-tracker
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Create a superuser

```powershell
python manage.py createsuperuser
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🔐 Environment Variables

For production, the application uses environment variables for sensitive configuration.

Example:

```text
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com
DATABASE_URL=your-postgresql-database-url
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

> Never commit your production secret key, database credentials, or `.env` file to GitHub.

## 🗄️ Database

The project uses:

* **SQLite** during local development.
* **PostgreSQL** in production.

Django's ORM is used for database operations, making it possible to work with the database using Python models instead of writing SQL for every operation.

## 🚀 Deployment

The project is deployed using **Render**.

Production setup includes:

```text
Django
   ↓
Gunicorn
   ↓
Render
   ↓
PostgreSQL
```

Static files are served using **WhiteNoise**.

The production application is configured with:

* `DEBUG=False`
* Environment-based secret key
* PostgreSQL database
* HTTPS
* Secure session cookies
* Secure CSRF cookies
* HSTS
* Gunicorn
* WhiteNoise

## 🧠 What I Learned

While building this project, I worked with:

* Django project and app architecture
* Django models and migrations
* Django forms
* Django authentication
* CRUD operations
* Django templates
* URL routing
* PostgreSQL integration
* Environment variables
* Static file configuration
* WhiteNoise
* Gunicorn
* Git and GitHub
* Production deployment
* Render deployment
* Basic production security configuration

## 🔮 Future Improvements

Some possible improvements include:

* Job search and filtering
* Dashboard with application statistics
* Application reminders
* Email notifications
* Resume management
* Interview scheduling
* Job priority levels
* Analytics and charts
* REST API using Django REST Framework
* Docker support

## 👨‍💻 Author

**Md Nawaz Khan**

GitHub:
https://github.com/mdnawaz78

---

⭐ If you find this project useful, feel free to explore the repository and try the application.
