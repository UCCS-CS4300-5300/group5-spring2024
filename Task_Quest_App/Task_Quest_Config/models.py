'''
Data Models for TaskQuest Application 
'''
from django.db import models

# We need a model for tasks: Date/Time/Name/Difficulty/Description/Status

# We need a model for users: Username/Email/Password

class tasks(models.Model):
  date = models.DateField()
  time = models.TimeField()
  name = models.CharField(max_length=100)
  diffo