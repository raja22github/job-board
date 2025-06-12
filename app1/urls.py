from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
]
