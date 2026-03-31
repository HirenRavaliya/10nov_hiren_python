from django.shortcuts import render
def index(request):
    return render(request, 'q3_js_val/index.html', {'title': 'Q3: JS Form Validation'})