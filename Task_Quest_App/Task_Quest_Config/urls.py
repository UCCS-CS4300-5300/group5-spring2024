"""
URL configuration for Task_Quest project.
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
  path('', views.calendar, name='calendar'),
  path('tasks/', views.TaskListView.as_view(), name='task-list'),
  path('addtask/', views.create_task, name='add-task')

]
