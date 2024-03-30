''' 
Views for Pages of the TaskQuest Application 
'''

from django.http import HttpResponse
from django.views import View, generic
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from datetime import datetime
from calendar import HTMLCalendar
from .models import Task
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required
def calendar(request):

  '''
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.user= request.user
      task.save()
      return redirect('index')

  else:
    form = TaskForm()
  '''
  # Create an instance of HTMLCalendar
  cal = HTMLCalendar()
  
  # Generate HTML for the current month's calendar
  html_cal = cal.formatmonth(datetime.today().year, datetime.today().month,     withyear=True)
  # Mark the HTML as safe to prevent autoescaping
  calendar = mark_safe(html_cal)
  # Get the current month and year in a human-readable format
  current_month_year = datetime.today().strftime('%B %Y')
  # Render the template with the calendar and current month/year as context  variables
  return render(request, 'Task_Quest_Config/calendar.html', {'calendar' : calendar, 'current_month_year': current_month_year})


'''This page doesn't work with the built-in webview since it uses an anonymous user. 
  Instead, use a new tab logged in as an admin user.'''
@method_decorator(login_required, name='dispatch')
class TaskListView(generic.ListView):
  model = Task
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['task_list'] = Task.objects.filter(user=self.request.user)
    context['current_user'] = self.request.user.username
    return context

@login_required
def create_task(request):
  form = TaskForm

  if request.method == 'POST':
    # Create a new dictionary with form data and movie_title
    task_data = request.POST.copy()
    form = TaskForm(task_data, request.FILES)
    if form.is_valid():
      # Save the form without committing to the database
      task = form.save(commit=False)
      # Set the user relationship
      task.user = request.user
      task.save()
      # Redirect back to the calendar page
      return redirect('task-list')
  context = {'form': form}
  return render(request, 'Task_Quest_Config/task_form.html', context)


@login_required
def home_page(request):
  top_tasks = Task.objects.filter(user=request.user)[:3]
  context = {'top_tasks' : top_tasks}
  return render(request, 'Task_Quest_Config/home.html', context)