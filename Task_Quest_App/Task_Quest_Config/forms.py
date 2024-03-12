from logging import PlaceHolder
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
  
  class Meta:
    model = Task
    fields = ['date', 'time', 'name', 'difficulty', 'priority']
    CHOICES = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5"}
    labels = {
        "name": _("Task Name"),
    }
    widgets = {
        "name" : forms.TextInput(attrs={'placeholder': 'Task Name'}),
        "date" : forms.DateInput(attrs={'type': 'date'}),
        "time" : forms.TimeInput(attrs={'type': 'time'}),
        #"difficulty" : forms.RadioSelect(choices=CHOICES.items(), attrs={'type': 'inline-block'}),
        "difficulty" : forms.Select(choices=CHOICES.items(), attrs={'type': 'number'}),
        "priority" : forms.Select(choices=CHOICES.items())
      #choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    }
