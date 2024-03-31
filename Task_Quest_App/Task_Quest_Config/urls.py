"""
URL configuration for Task_Quest project.
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
  # Home
  path('', views.home_page, name='home'),
  
  # Varying Calendar Views
  path('calendar/', views.calendar, name='calendar'),  
  path('calendar/<int:year>/<int:month>/', views.calendar, name='calendar'),
  path('prev/<int:year>/<int:month>/', views.prev_month_view, name='prev_month'),
  path('next/<int:year>/<int:month>/', views.next_month_view, name='next_month'),
  
  # Task List and Add Task
  path('tasks/', views.TaskListView.as_view(), name='task-list'),
  path('addtask/', views.create_task, name='add-task'),
  
  # Game page 
  path('game/', views.start_game, name='quest-game'),

]

#urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)