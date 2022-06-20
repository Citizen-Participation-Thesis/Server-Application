from django.urls import path

from . import views

urlpatterns = [
    path('add_content', views.create_page, name='Add Content'),
    path('create_project', views.create_project, name='Create Project'),
    path('deploy_project', views.deploy_project, name='Deploy Project'),
    path('project_success', views.project_success, name='Project Success'),
    path('model_success', views.model_success, name='Model Success'),
    path('', views.project_success, name='Home')
]