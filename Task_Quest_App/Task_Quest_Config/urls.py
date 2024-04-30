
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
  path('edit-task/<int:task_id>/', views.edit_task, name='edit-task'),
  path('postpone-task/<int:task_id>/', views.postpone_task, name='postpone-task'),
  path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
  path('remove-task/<int:task_id>/', views.remove_task, name='remove_task'),

  # Game page 
  path('game/', views.start_game, name='quest-game'),

  # Points Shop page 
  path('shop/', views.shop, name='shop'), 
  path('buy-item/<int:item_id>/', views.buy_item, name='buy_item'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)