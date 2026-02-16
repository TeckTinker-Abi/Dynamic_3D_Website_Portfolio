from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    
    # System Universe
    path('system/', views.system_universe, name='system_universe'),
    path('system/node/add/', views.node_edit, name='node_add'),
    path('system/node/<int:pk>/', views.node_edit, name='node_edit'),
    path('system/node/delete/<int:pk>/', views.node_delete, name='node_delete'),
    path('system/connection/add/', views.connection_edit, name='connection_add'),
    path('system/connection/<int:pk>/', views.connection_edit, name='connection_edit'),

    # Projects
    path('projects/', views.projects_list, name='projects'),
    path('projects/add/', views.project_edit, name='project_add'),
    path('projects/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),

    # Categories
    path('categories/', views.categories_list, name='categories'),
    path('categories/add/', views.category_edit, name='category_add'),
    path('categories/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Dashboard Content
    # Dashboard Content
    path('identity/', views.identity_core_view, name='identity_core'),
    path('live-system/', views.live_system_view, name='live_system'),
    path('content/', views.dashboard_content, name='dashboard_content'),
    path('content/metric/add/', views.metric_edit, name='metric_add'),
    path('content/metric/<int:pk>/', views.metric_edit, name='metric_edit'),
    path('content/capability/add/', views.capability_edit, name='capability_add'),
    path('content/capability/<int:pk>/', views.capability_edit, name='capability_edit'),
    path('content/focus/add/', views.current_focus_edit, name='focus_add'),
    path('content/focus/<int:pk>/', views.current_focus_edit, name='focus_edit'),
    path('content/focus/delete/<int:pk>/', views.current_focus_delete, name='focus_delete'),

    # Settings
    path('settings/', views.global_settings, name='global_settings'),

    # Tech Stack
    path('tech-stack/', views.tech_stack_view, name='tech_stack'),
    path('tech-stack/category/add/', views.tech_category_edit, name='tech_category_add'),
    path('tech-stack/category/<int:pk>/', views.tech_category_edit, name='tech_category_edit'),
    path('tech-stack/category/delete/<int:pk>/', views.tech_category_delete, name='tech_category_delete'),
    path('tech-stack/technology/add/', views.technology_edit, name='technology_add'),
    path('tech-stack/technology/<int:pk>/', views.technology_edit, name='technology_edit'),
    path('tech-stack/technology/delete/<int:pk>/', views.technology_delete, name='technology_delete'),
]
