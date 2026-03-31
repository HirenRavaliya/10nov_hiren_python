from django.shortcuts import render
def index(request):
    return render(request, 'q10_js_reg/index.html')