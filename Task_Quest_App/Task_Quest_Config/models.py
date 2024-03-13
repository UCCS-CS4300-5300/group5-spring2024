'''
Data Models for TaskQuest Application 
'''
from django.db import models
from django.contrib.auth.models import User

# We need a model for tasks: Date/Time/Name/Difficulty/Description/Status

# We need a model for users: Username/Email/Password
#Django has a built-in user model so we don't need to create our own

class Task(models.Model):
  date = models.DateField()
  time = models.TimeField()
  name = models.CharField(max_length=100)
  difficulty = models.IntegerField()
  priority = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  points = models.IntegerField(default=0)

  def __str__(self):
    return self.name