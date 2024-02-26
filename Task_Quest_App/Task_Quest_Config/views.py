''' 
Views for Pages of the TaskQuest Application 
'''

from django.http import HttpResponse
from django.views import View


# This will be REPLACED with the view of our home-page 
def index(request):
  return HttpResponse("This will be the home page...hopefully soon....?")


# We need to create a view of the calendar 