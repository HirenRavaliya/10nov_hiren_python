from django.http import JsonResponse


def api_root(request):
    """Landing page – lists all available API endpoints."""
    base = request.build_absolute_uri('/')[:-1]  # e.g. http://127.0.0.1:8000
    return JsonResponse({
        "message": "Welcome to EduTracker Solutions API",
        "version": "1.0",
        "endpoints": {
            "auth": {
                "obtain_token":  f"{base}/api/token/",
                "refresh_token": f"{base}/api/token/refresh/",
            },
            "students": {
                "list_create":    f"{base}/api/students/",
                "detail":         f"{base}/api/students/{{id}}/",
                "enrolled_courses": f"{base}/api/students/{{id}}/courses/",
                "enroll":         f"{base}/api/students/{{id}}/enroll/",
                "unenroll":       f"{base}/api/students/{{id}}/unenroll/{{course_id}}/",
            },
            "courses": {
                "list_create": f"{base}/api/courses/",
                "detail":      f"{base}/api/courses/{{id}}/",
            },
            "admin": f"{base}/admin/",
        }
    }, json_dumps_params={'indent': 2})
