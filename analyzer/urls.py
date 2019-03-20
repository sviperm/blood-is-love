from django.urls import include, path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.upload_file, name='home'),
    # path('analyzer/', views.analyzer, name='analyzer'),
]
