# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    @classmethod
    def tasks_for_date(cls, date):
        return cls.objects.filter(date=date)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  total_points = models.IntegerField(default=0)
  longest_game = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Item(models.Model):
  name = models.CharField(max_length=100)
  cost = models.IntegerField(default=0)
  description = models.TextField()
  image = models.ImageField(upload_to='item_images/',       default='item_images/default.jpg')

  def __str__(self):
      return self.name

class PurchasedItem(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  purchase_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f'{self.user.username} purchased {self.item.name}'