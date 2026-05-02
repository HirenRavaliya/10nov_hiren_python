# EduTracker Solutions – Student & Course Management API

A RESTful API built with **Django** and **Django REST Framework** to manage students and their enrolled courses.

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd module17assesment
```

### 2. Create & activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` → `.env` and fill in your values:
```bash
cp .env.example .env
```

### 5. Run migrations & create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the dev server
```bash
python manage.py runserver
```

---

## 📡 API Endpoints

### Authentication (JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain access + refresh tokens |
| POST | `/api/token/refresh/` | Refresh access token |

> Pass the access token in the `Authorization` header:  
> `Authorization: Bearer <access_token>`

---

### Students – `/api/students/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create a new student |
| GET | `/api/students/{id}/` | Get a single student |
| PUT | `/api/students/{id}/` | Full update |
| PATCH | `/api/students/{id}/` | Partial update |
| DELETE | `/api/students/{id}/` | Delete a student |
| GET | `/api/students/{id}/courses/` | List enrolled courses |
| POST | `/api/students/{id}/enroll/` | Enrol in a course |
| DELETE | `/api/students/{id}/unenroll/{course_id}/` | Remove from a course |

#### Create Student – Example payload
```json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice@example.com",
  "phone": "9876543210",
  "gender": "F",
  "date_of_birth": "2002-05-14",
  "course_ids": [1, 2]
}
```

---

### Courses – `/api/courses/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | List all courses |
| POST | `/api/courses/` | Create a new course |
| GET | `/api/courses/{id}/` | Get a single course |
| PUT | `/api/courses/{id}/` | Full update |
| PATCH | `/api/courses/{id}/` | Partial update |
| DELETE | `/api/courses/{id}/` | Delete a course |

#### Create Course – Example payload
```json
{
  "name": "Introduction to Python",
  "code": "CS101",
  "description": "Foundations of Python programming.",
  "credits": 4
}
```

---

## 🛡 Admin Panel

Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) after creating a superuser.

---

## 🗂 Project Structure

```
module17assesment/
├── edutracker/          # Django project config
│   ├── settings.py
│   └── urls.py
├── students/            # Student app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── courses/             # Course app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── venv/                # Virtual environment (gitignored)
├── .env                 # Secrets (gitignored)
├── .gitignore
├── requirements.txt
└── manage.py
```

---

## 🌐 Deployment (PythonAnywhere)

1. Upload code or clone from GitHub.
2. Create a virtual environment on PythonAnywhere and install `requirements.txt`.
3. Set `DEBUG=False` and update `ALLOWED_HOSTS` with your PA domain in `.env`.
4. Configure the WSGI file to point to `edutracker/wsgi.py`.
5. Run `python manage.py collectstatic`.

---

## 🧪 Testing with Postman / curl

```bash
# Get JWT token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# List students (authenticated)
curl http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Bearer <access_token>"

# Create a course
curl -X POST http://127.0.0.1:8000/api/courses/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Django Basics","code":"DJ101","credits":3}'
```
