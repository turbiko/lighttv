from django.urls import path

from .views import chart_page, upload_chart

urlpatterns = [
    path('', chart_page, name='chart'),
    path('upload/', upload_chart, name='upload_chart'),
]