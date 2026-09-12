# Lumen

![Lumen Architecture](assets/architecture.png)
A simple healthcare backend built with Django, Django REST Framework,
PostgreSQL and JWT authentication.


## Architecture Diagram

                    ┌─────────────────┐
                    │     Client      │
                    │    / Postman    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Django REST   │
                    │      API        │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌───────────┐  ┌─────────────┐
        │ Accounts │   │ Healthcare│  │ JWT Auth    │
        └──────────┘   └───────────┘  └─────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └─────────────────┘

## What it does

- Register users with name, email and password
- Log users in and return JWT access/refresh tokens
- Create and manage patients
- Create and manage doctors
- Assign doctors to patients
- Protect healthcare APIs with JWT authentication
- Keep patient records private to the user who created them
- Validate common input errors
- Store database credentials in environment variables

## Project structure

```text
lumen/
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├──assests/
|  ├── architecture.png
├── healthcare/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup on Windows

Create the PostgreSQL database first:

```sql
CREATE DATABASE lumen_db;
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your PostgreSQL password in it.

Then run:

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Open:

`http://127.0.0.1:8000/`

## API endpoints

### Authentication

```text
POST /api/auth/register/
POST /api/auth/login/
```

### Patients

```text
POST   /api/patients/
GET    /api/patients/
GET    /api/patients/<id>/
PUT    /api/patients/<id>/
DELETE /api/patients/<id>/
```

### Doctors

```text
POST   /api/doctors/
GET    /api/doctors/
GET    /api/doctors/<id>/
PUT    /api/doctors/<id>/
DELETE /api/doctors/<id>/
```

### Patient-doctor mappings

```text
POST   /api/mappings/
GET    /api/mappings/
GET    /api/mappings/<patient_id>/
DELETE /api/mappings/<id>/
```

For protected requests use:

```text
Authorization: Bearer <access_token>
```

## Example registration

```json
{
    "name": "Aayush",
    "email": "aayush@example.com",
    "password": "StrongPassword123"
}
```

## Example login

```json
{
    "email": "aayush@example.com",
    "password": "StrongPassword123"
}
```

The login response contains `access` and `refresh` tokens.

## Example patient

```json
{
    "name": "Rahul Sharma",
    "age": 32,
    "gender": "Male",
    "address": "Pune, Maharashtra",
    "phone": "9876543210",
    "medical_history": "No major medical history"
}
```

## Example doctor

```json
{
    "name": "Dr. Neha Patil",
    "specialization": "Cardiology",
    "email": "neha@example.com",
    "phone": "9876543211",
    "experience_years": 8
}
```

## Example mapping

```json
{
    "patient": 1,
    "doctor": 1
}
```

A patient can have multiple doctors, but the same doctor cannot be
assigned to the same patient twice.
