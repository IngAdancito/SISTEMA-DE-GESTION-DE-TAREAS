from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_tasks_csv, name='export_tasks'),
]
