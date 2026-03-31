from django.shortcuts import render
def index(request):
    return render(request, 'q2_css/index.html', {'title': 'Q2: CSS Styled Template'})