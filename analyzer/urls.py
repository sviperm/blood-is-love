from django.urls import include, path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.home, name='home'),
    path('analyzer/', views.analyzer, name='analyzer'),
    path('about/', views.about, name='about'),
]
