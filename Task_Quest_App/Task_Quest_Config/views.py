from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserProfile  # Import UserProfile model
from .models import Task
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@login_required
def home(request):
      user_profile = None

      try:
          # Retrieve user profile if authenticated
          if request.user.is_authenticated:
              user_profile = UserProfile.objects.get(user=request.user)
      except UserProfile.DoesNotExist:
          pass

      tasks = Task.objects.all()
      completed_tasks = tasks.filter(completed=True)

      total_points = completed_tasks.count() * 10  # Each completed task is worth 10 points

      if tasks.exists():
          completion_percentage = (completed_tasks.count() / tasks.count()) * 100
      else:
          completion_percentage = 0

      # Get the username of the logged-in user
      username = request.user.username if request.user.is_authenticated else None

      # Pass the username, points, total_points, and completion_percentage to the template context
      return render(request, 'home.html', {
          'user_profile': user_profile,
          'tasks': tasks,
          'total_points': total_points,
          'completion_percentage': completion_percentage,
          'points': user_profile.points if user_profile else 0,
          'username': username  # Pass the username to the template context
      })




def contact_us(request):
    return render(request, 'contact_us.html')









@login_required
def todo_list(request):
      user_profile = None

      try:
          # Retrieve user profile if authenticated
          if request.user.is_authenticated:
              user_profile = UserProfile.objects.get(user=request.user)
      except UserProfile.DoesNotExist:
          pass

      tasks = Task.objects.all()
      completed_tasks = tasks.filter(completed=True)

      total_points = completed_tasks.count() * 10  # Each completed task is worth 10 points

      if tasks.exists():
          completion_percentage = (completed_tasks.count() / tasks.count()) * 100
      else:
          completion_percentage = 0

      if request.method == 'POST':
          # Handle form submission to mark tasks as completed
          for task in tasks:
              task_id = request.POST.get('task_id_' + str(task.id))
              task_complete = request.POST.get('task_' + str(task.id), False)

              if task_id and task_complete:
                  task.completed = True
                  task.save()

          # Render the todo_list.html template instead of redirecting to home
          return render(request, 'todo_list.html', {'user_profile': user_profile, 'tasks': tasks, 'total_points': total_points, 'completion_percentage': completion_percentage, 'points': user_profile.points if user_profile else 0})

      # Pass the points, total_points, and completion_percentage to the template context
      return render(request, 'todo_list.html', {'user_profile': user_profile, 'tasks': tasks, 'total_points': total_points, 'completion_percentage': completion_percentage, 'points': user_profile.points if user_profile else 0})
