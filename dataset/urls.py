from django.urls import include, path
from . import views

app_name = 'dataset'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
]
