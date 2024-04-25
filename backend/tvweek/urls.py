from django.urls import path

from .views import chart_page, upload_chart, get_current_time

urlpatterns = [
    path('', chart_page, name='chart'),
    path('upload/', upload_chart, name='upload_chart'),
    path('get-current-time/', get_current_time, name='get-current-time'),
]