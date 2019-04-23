from django.urls import include, path
from .views import (DatasetView, DeleteView, PieChartView, UploadView,
                    dataset, single_image)

app_name = 'dataset'

urlpatterns = [
    path('', dataset, name='dataset'),
    path('page/<int:page_num>', DatasetView.as_view(), name='dataset_page'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('delete_image/', DeleteView.as_view(), name='delete_image'),
    path('image-<int:id>/', single_image, name='single_image'),
]
