"""
URL configuration for Task_Quest project.
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
  path('', views.calendar, name='calendar'),
  path('calendar/<int:year>/<int:month>/', views.calendar, name='calendar'),
  path('prev/<int:year>/<int:month>/', views.prev_month_view, name='prev_month'),
  path('next/<int:year>/<int:month>/', views.next_month_view, name='next_month'),
  
  path('tasks/', views.TaskListView.as_view(), name='task-list'),
  path('addtask/', views.create_task, name='add-task')

]
