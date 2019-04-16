from django.urls import include, path
from . import views

app_name = 'dataset'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('delete_image/', views.DeleteView.as_view(), name='delete_image'),
    path('image-<int:id>/', views.single_image, name='single_image'),
]
