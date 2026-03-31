from django.shortcuts import render
def index(request):
    return render(request, 'q8_admin/index.html')