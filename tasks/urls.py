from django.urls import path

from . import views


app_name = 'tasks'
urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('new_task/', views.new_task, name='new_task'),
]
