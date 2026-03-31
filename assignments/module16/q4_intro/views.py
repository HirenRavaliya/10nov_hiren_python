from django.shortcuts import render
def index(request):
    return render(request, 'q4_intro/index.html', {'title': 'Q4: Simple Django Webpage', 'message': 'Hello from Django!'})