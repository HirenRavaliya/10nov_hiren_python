from django.shortcuts import render
from .models import Article

def index(request):

    articles = Article.objects.all()[:5]

    context = {
        'articles': articles,
        'total_articles': Article.objects.count(),
    }

    return render(request, 'q7_mvt/index.html', context)