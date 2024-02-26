''' 
Views for Pages of the TaskQuest Application 
'''

from django.http import HttpResponse
from django.views import View, generic
from .models import Task


# This will be REPLACED with the view of our home-page 
def index(request):
  return HttpResponse("This will be the home page...hopefully soon....?")


# We need to create a view of the calendar 

'''This page doesn't work with the built-in webview since it uses an anonymous user. 
  Instead, use a new tab logged in as an admin user.'''
class TaskListView(generic.ListView):
  model = Task
  def get_context_data(self, **kwargs): #def get_queryset(self
    context = super().get_context_data(**kwargs)
    context['task_list'] = Task.objects.filter(user=self.request.user)
    context['current_user'] = self.request.user.username
    return context