''' 
Views for Pages of the TaskQuest Application 
'''

from django.http import HttpResponse
from django.views import View, generic
from django.shortcuts import render
from django.utils.safestring import mark_safe
from datetime import datetime
from calendar import HTMLCalendar
from .models import Task


# This will be REPLACED with the view of our home-page 
def index(request):
  cal = HTMLCalendar()
  html_cal = cal.formatmonth(datetime.today().year, datetime.today().month, withyear=True)
  html_cal = html_cal.replace('<td ', '<td height=100')
  html_cal = html_cal.replace('<th ', '<th width=150')
  calendar = mark_safe(html_cal)
  #calendar = calendar.replace('<td ', '<td  width="150" height="150"')
  current_month_year = datetime.today().strftime('%B %Y')
  return render(request, 'Task_Quest_Config/index.html', {'calendar' : calendar, 'current_month_year': current_month_year})


'''This page doesn't work with the built-in webview since it uses an anonymous user. 
  Instead, use a new tab logged in as an admin user.'''
class TaskListView(generic.ListView):
  model = Task
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['task_list'] = Task.objects.filter(user=self.request.user)
    context['current_user'] = self.request.user.username
    return context

