from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from dataset.views import DeleteView, PieChartView, UpdateCountView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analyzer.urls', namespace='analyzer')),
    path('dataset/', include('dataset.urls', namespace='dataset')),
    # API
    path('api/', include([
        path('get-pie-chart/', PieChartView.as_view(), name="api_chart"),
        path('delete-image/', DeleteView.as_view(), name="api_delete"),
        path('update-stat/', UpdateCountView.as_view(), name="api_update_count"),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
