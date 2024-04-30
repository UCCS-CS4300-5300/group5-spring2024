''' 
Views for Pages of the TaskQuest Application 
'''

from django.shortcuts import render, redirect
from datetime import datetime
from calendar import HTMLCalendar
from .models import *
from .forms import *
from django.views import generic  # Add this import
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta

from django.core.serializers import serialize
from datetime import date
from django.utils import timezone
from django.db import transaction

from dateutil.relativedelta import relativedelta

from django.contrib import messages




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
    points = Profile.objects.get(user=self.request.user)
    context['total_points'] = points.total_points
    return context


@login_required
def create_task(request):
  #form = TaskForm
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
  #prevent older dates to be selected in the task form
  today_date = date.today().strftime('%Y-%m-%d')
  context = {'today_date': today_date}
  return render(request, 'Task_Quest_Config/task_form.html', context)


@login_required
def edit_task(request, task_id):
  # Edit task information other than the time and date
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    # Create a new dictionary with form data and movie_title
    task_data = request.POST.copy()
    form = TaskForm(task_data, request.FILES, instance=task)
    form.data['time'] = task.time
    form.data['date'] = task.date
    if form.is_valid():
      # Save the form without committing to the database
      task = form.save(commit=False)
      # Set the user relationship
      task.user = request.user
      task.save()
      # Redirect back to the calendar page
      return redirect('task-list')
  #show form for editing task
  context = {'task' : task}
  return render(request, 'Task_Quest_Config/edit_task_form.html', context)

@login_required
def postpone_task(request, task_id):
  # Postpone a task and add a penalty of  Total Points = Total Points - (0.25 * Task Points)
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  old_task = Task.objects.get(pk=task_id, user=request.user)
  if request.method == 'POST':
    # Create a new dictionary with form data and movie_title
    form = TaskForm(request.POST.copy(), request.FILES, instance=task)
    form.data['name'] = task.name
    form.data['difficulty'] = task.difficulty
    form.data['priority'] = task.priority
    form.data['points'] = task.points
    if form.is_valid():
      new_datetime = datetime.combine(task.date, task.time)
      if new_datetime > datetime.combine(old_task.date, old_task.time):
        with transaction.atomic():
          try:
            # Calculate point deduction
            profile = Profile.objects.select_for_update().get(user=request.user)
            penalty = int(0.25 * task.points)
            #save the new total points
            profile.total_points -= max(penalty, 0)
            profile.save()
            # save task data
            task.save()
          except Exception as e:
            print(e)
            transaction.set_rollback(True)
      else:
        messages.error(request, 'The new time must be after the old time.')
  # Redirect back to the calendar page
  return redirect('task-list')

def start_game(request):
  gameData = {'points': request.user.profile.total_points}
  if request.method == 'POST':
    # Create a new dictionary with form data and movie_title
    game_data = request.POST.copy()
    if float(game_data.get('inputName')) > request.user.profile.longest_game:
      request.user.profile.longest_game = game_data.get('inputName')
      request.user.profile.save()
      
  return render(request, 'Task_Quest_Config/game.html', gameData)

@login_required
def home_page(request):
    top_tasks = Task.objects.filter(user=request.user)[:3]
    points = Profile.objects.get(user=request.user)
    purchased_items = PurchasedItem.objects.filter(user=request.user)  # Retrieve purchased items
    serialized_tasks = serialize('json', top_tasks)
    context = {
        'top_tasks': top_tasks, 
        'total_points': points.total_points,
        'longest_game': points.longest_game,
        'serialized_tasks': serialized_tasks,
        'purchased_items': purchased_items  # Add to context
    }
    return render(request, 'Task_Quest_Config/home.html', context)


@login_required
def remove_task(request, task_id):
  # Retrieve task from database
  task = get_object_or_404(Task, id=task_id)
  # Check if the task belongs to the current user
  if task.user == request.user:
    with transaction.atomic():
      try:
        #apply penalty for deleting task
        profile = Profile.objects.get(user=request.user)
        penalty = profile.total_points - task.points
        profile.total_points = max(penalty, 0)
        profile.save()
        # Delete the task
        task.delete()
      except Exception as e:
        print(e)
        transaction.set_rollback(True)        
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

@login_required
def shop(request):
    items = Item.objects.all()
    return render(request, 'Task_Quest_Config/shop.html', {'items': items})

@login_required
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    profile = Profile.objects.get(user=request.user)

    # Check if the item has already been purchased by the user
    already_purchased = PurchasedItem.objects.filter(user=request.user, item=item).exists()

    if already_purchased:
        messages.error(request, f'You have already purchased {item.name}.')
        return redirect('shop')

    if profile.total_points >= item.cost:
        profile.total_points -= item.cost
        profile.save()
        PurchasedItem.objects.create(user=request.user, item=item)  # Record the purchase
        messages.success(request, f'You have successfully purchased {item.name}.')
    else:
        messages.error(request, 'Insufficient points to purchase this item.')

    return redirect('shop')
