from django.urls import path
from . import views

urlpatterns = [
    path('<slug:category_slug>/', views.category_projects, name='category_projects'),
    path('<slug:category_slug>/<slug:project_slug>/', views.project_detail, name='project_detail'),
]
