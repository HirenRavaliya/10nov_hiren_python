from django.shortcuts import render
from datetime import datetime

def index(request):
    context = {
        'title': 'Q1: HTML Template Rendering',
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'student_name': 'John Doe',
        'course': 'Django Web Development',
        'topics': ['Template Syntax', 'Context Variables', 'Template Tags', 'Template Filters', 'Template Inheritance'],
        'is_enrolled': True,
    }
    return render(request, 'q1_html/index.html', context)