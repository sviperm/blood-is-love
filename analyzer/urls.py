from django.urls import include, path
from analyzer import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.index, name='home'),
]
