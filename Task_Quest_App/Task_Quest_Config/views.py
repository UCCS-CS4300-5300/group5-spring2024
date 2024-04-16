''' 
Views for Pages of the TaskQuest Application 
'''

from django.shortcuts import render, redirect
from datetime import datetime
from calendar import HTMLCalendar
from .models import Task
from .forms import TaskForm
from django.views import generic  # Add this import
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Profile

from dateutil.relativedelta import relativedelta

from django.core.serializers import serialize
import json

from dateutil.relativedelta import relativedelta



@login_required
def calendar(request, year=None, month=None):
    current_date = datetime.today()
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

    # Calculate the previous month
    prev_month_date = current_date.replace(year=year, month=month, day=1) - relativedelta(months=0)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month

    # Calculate the next month
    next_month_date = current_date.replace(year=year, month=month, day=1) + relativedelta(months=0)
    next_year = next_month_date.year
    next_month = next_month_date.month

    # Generate the HTML for the calendar
    cal = HTMLCalendar()
    html_cal = cal.formatmonth(year, month, withyear=True)

    # Get the list of days in the month
    days = cal.itermonthdays(year, month)

    # Create a list to hold the calendar days and associated tasks
    calendar_days = []

    # Query tasks for the current month and year
    tasks = Task.objects.filter(user=request.user, date__year=year, date__month=month)

    # Loop through the days of the month and create a dictionary for each day
    for day in days:
        day_tasks = tasks.filter(date__day=day)
        calendar_days.append({'day_number': day, 'tasks': day_tasks, 'is_today': day == current_date.day})

    # Pass the current month and year to the template
    current_month_year = datetime(year, month, 1).strftime('%B %Y')

    return render(request, 'Task_Quest_Config/calendar.html', {
        'calendar': html_cal,
        'current_month_year': current_month_year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'calendar_days': calendar_days,
    })

from django.urls import reverse

def prev_month_view(request, year, month):
  # Calculate the previous month's year and month
  prev_year = int(year)
  prev_month = int(month) - 1
  if prev_month == 0:
      prev_month = 12
      prev_year -= 1

  # Redirect to the previous month's calendar view
  return redirect(reverse('calendar', kwargs={'year': prev_year, 'month': prev_month}))

def next_month_view(request, year, month):
  # Calculate the next month's year and month
  next_year = int(year)
  next_month = int(month) + 1
  if next_month == 13:  # If next month is December, reset to January of the next year
      next_month = 1
      next_year += 1

  # Redirect to the next month's calendar view
  return redirect(reverse('calendar', kwargs={'year': next_year, 'month': next_month}))


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
  points =  Profile.objects.get(user=request.user)
  serialized_tasks = serialize('json', top_tasks) 
  context = {'top_tasks': top_tasks, 'total_points': points.total_points, 
             'serialized_tasks': serialized_tasks}
  return render(request, 'Task_Quest_Config/home.html', context)


@login_required
def remove_task(request, task_id):
  # Retrieve task from database
  task = get_object_or_404(Task, id=task_id)

  # Check if the task belongs to the current user
  if task.user == request.user:
    task.delete()
    return redirect('task-list')
  else:
    # If the task doesn't belong to the current user just redirect to task list page
    return redirect('task-list')


@login_required
def complete_task(request, task_id):
    # Retrieve task from database
    task = get_object_or_404(Task, id=task_id)

    # Check if the task belongs to the current user
    if task.user == request.user:
        # Increment the points for the user
        profile = Profile.objects.get(user=request.user)
        profile.total_points += task.points
        profile.save()

        # Remove task and redirect back to home page
        task.delete()
        return redirect('home')  # Redirect to the home page
    else:
        # If the task doesn't belong to the current user just redirect to task list page
        return redirect('task-list')
