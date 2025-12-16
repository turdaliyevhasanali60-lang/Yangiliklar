from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from .models import *
import datetime



class HomeView(View):
    def get(self, request):
        main_articles = Article.objects.order_by('-important', "-views")[:9]
        today = datetime.date.today()
        latest_articles = Article.objects.order_by('created_at', "-views")[:10]

        top5_categories = Category.objects.annotate(
            article_count=Count('articles'),
        ).order_by('-article_count')[:5]

        top5_categories_articles = []

        for category in top5_categories:
            top5_categories_articles.append(
                Article.objects.filter(category=category).order_by('-important', '-views')[:6]
            )

        most_views = Article.objects.order_by('-views')[:10]

        moments = Moment.objects.filter(
            published=True
        ).exclude(
            photo=''  # Exclude empty photo field
        ).order_by('-created_at')


        context = {
            'main_articles': main_articles,
            'today': today,
            'latest_articles': latest_articles,
            'top5_categories': top5_categories,
            'top5_categories_articles': top5_categories_articles,
            "most_views": most_views,
            'moments': moments,
        }
        return render(request, 'index.html', context)


class ArticleDetailsView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        contexts = article.context.all().order_by('id')

        like_articles = Article.objects.exclude(slug=slug).filter(
            category=article.category
        ).order_by('-created_at')[:10]

        comments = Comment.objects.filter(
            article=article,
            published=True
        ).order_by('-created_at')

        context = {
            "article": article,
            "contexts": contexts,
            "like_articles": like_articles,
            "comments": comments,
        }
        return render(request, 'detail-page.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        Comment.objects.create(
            article=article,
            name=request.POST['name'],
            email=request.POST['email'],
            text=request.POST.get('text'),
        )
        return redirect('article-details', slug=slug)

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')


class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)

        category_articles = Article.objects.filter(
            category=category,
            published=True
        ).order_by('-important', "-created_at")

        popular_articles = Article.objects.filter(
            published=True
        ).order_by( "-views")[:10]

        latest_articles = Article.objects.filter(
            published=True
        ).order_by('-created_at')[:5]

        context = {
            'category': category,
            'category_articles': category_articles,
            'popular_articles': popular_articles,
            'latest_articles': latest_articles,
            'total_articles': Article.objects.count(),
        }
        return render(request, 'category.html', context)