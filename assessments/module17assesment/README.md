# EduTracker Solutions – Student & Course Management API

A RESTful API built with **Django** and **Django REST Framework** to manage students and their enrolled courses.

This project is deployed live on PythonAnywhere. The base API URL is:

**[https://studentapi.pythonanywhere.com/api/students/](https://studentapi.pythonanywhere.com/api/students/)**

---

## API Endpoints

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
  "first_name": "Hiren ",
  "last_name": "Ravaliya",
  "email": "hirenravaliya45@gmail.com",
  "phone": "9876543210",
  "gender": "M",
  "date_of_birth": "2003-04-11",
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

## Admin Panel

Visit [https://studentapi.pythonanywhere.com/admin/](https://studentapi.pythonanywhere.com/admin/) to access the Django admin panel.

---

## Project Structure

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

## Deployment (PythonAnywhere)

This project is live and accessible at **[https://studentapi.pythonanywhere.com/api/students/](https://studentapi.pythonanywhere.com/api/students/)**.

It is hosted on PythonAnywhere with the following configuration:
- Code is sourced from GitHub.
- A virtual environment is set up on PythonAnywhere with all dependencies from `requirements.txt` installed.
- `DEBUG=False` and `ALLOWED_HOSTS` is set to the PythonAnywhere domain in `.env`.
- The WSGI file points to `edutracker/wsgi.py`.
- Static files are collected using `python manage.py collectstatic`.

---

## Testing with Postman / curl

```bash
# Get JWT token
curl -X POST https://studentapi.pythonanywhere.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# List students (authenticated)
curl https://studentapi.pythonanywhere.com/api/students/ \
  -H "Authorization: Bearer <access_token>"

# Create a course
curl -X POST https://studentapi.pythonanywhere.com/api/courses/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Django Basics","code":"DJ101","credits":3}'
```
