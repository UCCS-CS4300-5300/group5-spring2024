
from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from .views import login_view

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),  # Redirect to login page by default
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('todo-list/', views.todo_list, name='todo_list'),  # Define URL pattern for todo list
]
