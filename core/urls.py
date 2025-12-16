from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('aloqa/', ContactView.as_view(), name='contact'),
    path('kategoriya/<slug:slug>', CategoryView.as_view(), name='category'),
    path('<slug:slug>/', ArticleDetailsView.as_view(), name='article-details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)