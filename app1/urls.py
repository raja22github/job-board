from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jobs/employer_dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<int:job_id>/', views.job_details, name='job_details'),
    path('jobs/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('seeker/dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('applications/<int:app_id>/edit/', views.edit_application, name='edit_application'),
    path('applications/<int:app_id>/delete/', views.delete_application, name='delete_application'),
    path('applications/<int:app_id>/<str:new_status>/', views.update_application_status, name='update_application_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
