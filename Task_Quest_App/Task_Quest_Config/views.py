''' 
Views for Pages of the TaskQuest Application 
'''

from django.http import HttpResponse
from django.views import View, generic
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Task
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required

def calendar(request, year=None, month=None):
  # Get the current date
  current_date = datetime.today()

  # If year and month parameters are provided in the URL, use them; otherwise, use the current date
  if year and month:
      try:
          year = int(year)
          month = int(month)
      except ValueError:
          year = current_date.year
          month = current_date.month
  else:
      year = current_date.year
      month = current_date.month

  # Calculate previous month and year
  prev_month_date = current_date.replace(year=year, month=month, day=1) - timedelta(days=1)
  prev_year = prev_month_date.year
  prev_month = prev_month_date.month

  # Calculate next month and year
  next_month_date = current_date.replace(year=year, month=month, day=28) + timedelta(days=4)
  next_year = next_month_date.year
  next_month = next_month_date.month

  # Create an instance of HTMLCalendar
  cal = HTMLCalendar()

  # Generate HTML for the specified month's calendar
  html_cal = cal.formatmonth(year, month, withyear=True)
  # Mark the HTML as safe to prevent autoescaping
  calendar = mark_safe(html_cal)
  
  # Get the current month and year in a human-readable format
  current_month_year = datetime(year, month, 1).strftime('%B %Y')

  return render(request, 'Task_Quest_Config/calendar.html', {
      'calendar': calendar,
      'current_month_year': current_month_year,
      'prev_month': prev_month,
      'prev_year': prev_year,
      'next_month': next_month,
      'next_year': next_year,
  })

def prev_month_view(request, year, month):
    # Redirect to the previous month's calendar view
    return redirect(reverse('calendar', kwargs={'year': year, 'month': month}))

def next_month_view(request, year, month):
    # Redirect to the next month's calendar view
    return redirect(reverse('calendar', kwargs={'year': year, 'month': month}))


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


def start_game(request):
  gameData = {'points': request.user.profile.total_points}
  return render(request, 'Task_Quest_Config/game.html', gameData)


@login_required
def home_page(request):
  top_tasks = Task.objects.filter(user=request.user)[:3]
  context = {'top_tasks' : top_tasks}
  return render(request, 'Task_Quest_Config/home.html', context)

