from django.shortcuts import render
def index(request):
    return render(request, 'q15_custom_admin/index.html')