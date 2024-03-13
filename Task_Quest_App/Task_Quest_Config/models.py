'''
Data Models for TaskQuest Application 
'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  total_points = models.IntegerField(default=0)

  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()