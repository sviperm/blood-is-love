from django.urls import include, path
from .views import (DatasetPagesView, DeleteView, PieChartView, UploadView,
                    DatasetView, single_image)

app_name = 'dataset'

urlpatterns = [
    path('', DatasetView.as_view(), name='dataset'),
    path('<str:type>/', include([
        path('page/<int:page_num >', DatasetPagesView.as_view(), name='dataset_view'),
        path('image-<int:id>/', single_image, name='single_image'),
    ])),
    path('upload/', UploadView.as_view(), name='upload'),
]
