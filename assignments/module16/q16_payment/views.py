from django.shortcuts import render
def index(request):
    return render(request, 'q16_payment/index.html')