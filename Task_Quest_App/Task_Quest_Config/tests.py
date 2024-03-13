from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from Task_Quest_App.Task_Quest_Config.models import Task
from django.urls import reverse


class TaskUnitTest(TestCase):
  def test_task_fields(self):

    # Create test data
    testUser = User.objects.create()
    
    testTask = Task.objects.create(name='Do Homework',
                                    date='2020-01-01',
                                    time='10:45',
                                    difficulty=2,
                                    priority=3,
                                    user = testUser)

    #Test the values for the Task fields
    self.assertEqual(testTask.name, 'Do Homework')
    self.assertEqual(testTask.date, '2020-01-01')
    self.assertEqual(testTask.time, '10:45')
    self.assertEqual(testTask.difficulty, 2)
    self.assertEqual(testTask.priority, 3)
    self.assertEqual(testTask.user, testUser)


class TaskListIntegrationTest(APITestCase):
  
    #Establishes context for integration test
    def setUp(self):
      self.client = APIClient()
      self.user = User.objects.get_or_create(username='Joe', password="JoeMama1")[0]
      self.client.force_login(self.user)
      self.url = reverse('task-list')
  
    #Create integration test
    def test_task_integration_sad(self):
  
      # Create test data
      testUser = User.objects.create()
      testTask = Task.objects.create(name='Do Homework',
                                      date='2020-01-01',
                                      time='10:45',
                                      difficulty=2,
                                      priority=3,
                                      user = testUser)
  
      # Send a GET request to the URL
      response = self.client.get(self.url)
  
  
      # Assert the response status code and content
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'No tasks to show.')
  
    #Create integration test
    def test_task_integration_happy(self):
  
      # Create test data
      testTask = Task.objects.create(name='Do Homework',
                                      date='2020-01-01',
                                      time='13:45',
                                      difficulty=2,
                                      priority=3,
                                      user = self.user)
  
      # Send a GET request to the URL
      response = self.client.get(self.url)
  
  
      # Assert the response status code and content
      self.assertEqual(response.status_code, 200)
      #Test the values for the Task fields
      self.assertContains(response, 'Name: Do Homework')
      self.assertContains(response, 'Date: Jan. 1, 2020')
      self.assertContains(response, 'Time: 1:45 p.m.')
      self.assertContains(response, 'Difficulty: 2')
      self.assertContains(response, 'Priority: 3')
      self.assertContains(response, 'Assigned to: Joe')