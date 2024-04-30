from django.test import TestCase, SimpleTestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from Task_Quest_App.Task_Quest_Config.models import *
from Task_Quest_App.Task_Quest_Config.views import *
from Task_Quest_App.Task_Quest_Config.forms import *
from django.urls import reverse, resolve
from datetime import datetime, date, time
from django.utils import timezone
from django.http import Http404 


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



class GameIntegrationTest(APITestCase):

    #Establishes context for integration test
    def setUp(self):
      self.client = APIClient()
      self.user = User.objects.get_or_create(username='Joe', password="JoeMama1")[0]
      self.user.profile.total_points = 321
      self.client.force_login(self.user)
      self.url = reverse('quest-game')

    #Create integration test
    def test_game_integration(self):

      # Create test data
      #testUser = User.objects.create()
      #testProfile = Profile.objects.create(user=self.user, total_points=20)
      #testTask = Task.objects.create(name='Do Homework',
      #                                date='2020-01-01',
      #                                time='10:45',
      #                                difficulty=2,
      #                                priority=3,
      #                                user = testUser)

      # Send a GET request to the URL
      response = self.client.get(self.url)


      # Assert the response status code and content
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'Points: 321')

class HomePageIntegrationTest(APITestCase):
  # create test data
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='TestUser', password="testPassword!")
    self.client.login(username='TestUser', password='testPassword!')
    self.task1 = Task.objects.create(user=self.user, name='Task 1', 
                                     date='2024-03-30', time='13:45', 
                                     difficulty=2, priority=3)
    self.task2 = Task.objects.create(user=self.user, name='Task 2', 
                                     date='2024-01-30',time='13:45', 
                                     difficulty=2, priority=3)
    self.task3 = Task.objects.create(user=self.user, name='Task 3', 
                                     date='2024-01-30', time='13:45',
                                     difficulty=2, priority=3)

  def test_home_page_view(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'Task_Quest_Config/home.html')
    self.assertContains(response, 'Task 1')
    self.assertContains(response, 'Task 2')
    self.assertContains(response, 'Task 3')

class PostponeTaskTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='TestUser', password="testPassword!")
    self.client.login(username='TestUser', password='testPassword!')
    self.task = Task.objects.create(user=self.user, name='Task 1', 
                                    date='2024-03-30', time='13:45', 
                                    difficulty=1, priority=1, points=100)
    self.profile = Profile.objects.get(user=self.user)
    self.profile.total_points = 500
    self.profile.save()

  def test_postpone_task(self):
    url = reverse('postpone-task', kwargs={'task_id': self.task.id})
    response = self.client.post(url,{
      'date': '2024-05-10',
      'time': '14:45',
    })
    # Check if the view redirects (302 status code)
    self.assertEqual(response.status_code, 302)

    # Check if the points were deducted correctly
    ## Refresh the profile from the database
    self.profile.refresh_from_db()
    expected_points = 500 - int(0.25 * self.task.points)
    self.assertEqual(self.profile.total_points, expected_points)

  def test_postpone_task_fail(self):
    url = reverse('postpone-task', kwargs={'task_id': self.task.id})
    #use date in the past, the postpone should fail
    response = self.client.post(url,{
      'date': '2024-02-10',
      'time': '14:45',
    })

    self.profile.refresh_from_db()
    expected_points = 500 - int(0.25 * self.task.points)
    self.assertNotEqual(self.profile.total_points, expected_points)

  def tearDown(self):
    # Clean up created objects after the test
    self.task.delete()
    self.user.delete()

class RemoveTaskTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='TestUser', password="testPassword!")
    self.client.login(username='TestUser', password='testPassword!')
    self.task = Task.objects.create(user=self.user, name='Task 1', 
                                    date='2024-03-30', time='13:45', 
                                    difficulty=1, priority=1, points=100)
    self.profile = Profile.objects.get(user=self.user)
    self.profile.total_points = 500
    self.profile.save()

  def test_remove_task(self):
    url = reverse('remove_task', kwargs={'task_id': self.task.id})
    response = self.client.post(url)

    # Check if the task is deleted and points are deducted
    with self.assertRaises(Http404):
       get_object_or_404(Task, id=self.task.id)  # Task should not exist after deletion

    profile_before = self.profile.total_points
    profile_after = Profile.objects.get(user=self.user).total_points
    # Check if the points are deducted
    self.assertNotEqual(profile_before, profile_after)
    # Check if points were deducted: 500 - 100 = 400
    self.assertEqual(profile_after, 400)

  def tearDown(self):
    # Clean up created objects after the test
    self.task.delete()
    self.user.delete()
  

# Unit Tests for indvidual models
class ModelUnitTest(TestCase):
  def setUp(self):
      # Create a user
      self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword123')
      # Create a task for the user
      self.task = Task.objects.create(
          date='2024-04-04',
          time='14:00',
          name='Test Task',
          difficulty=5,
          priority=2,
          user=self.user,
          points=10
      )

  def test_task_creation(self):
      """Test the task creation."""
      self.assertEqual(self.task.name, 'Test Task')
      self.assertEqual(self.task.user, self.user)
      self.assertEqual(self.task.points, 10)

  def test_profile_creation(self):
      """Test profile is created for a new user."""
      self.assertEqual(hasattr(self.user, 'profile'), True)
      self.assertEqual(self.user.profile.total_points, 0)

  def test_profile_update(self):
      """Test updating the user profile."""
      self.user.profile.total_points = 100
      self.user.profile.save()
      self.assertEqual(Profile.objects.get(user=self.user).total_points, 100)

  def tearDown(self):
      # Clean up after each test
      self.user.delete()
      self.task.delete()


# Unit Tests for individual views 
class ViewUnitCase(TestCase):
  def setUp(self):
      self.user = User.objects.create_user(username='testuser', password='12345')
      self.client = Client()
      self.client.login(username='testuser', password='12345')
      self.task = Task.objects.create(
          date=datetime.now().date(),
          time=datetime.now().time(),
          name='Test Task',
          difficulty=1,
          priority=1,
          user=self.user,
          points=10
      )

  def test_add_task_view_get(self):
      """Test the GET method for add_task view."""
      response = self.client.get(reverse('add-task'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'Task_Quest_Config/task_form.html')

  def test_add_task_view_post(self):
      """Test the POST method for add_task view."""
      response = self.client.post(reverse('add-task'), {
          'date': datetime.now().date(),
          'time': datetime.now().time(),
          'name': 'Another Test Task',
          'difficulty': 2,
          'priority': 2,
          'points': 20
      })
      self.assertRedirects(response, reverse('task-list'))
      self.assertEqual(Task.objects.count(), 2)

  def test_remove_task_view(self):
      """Test the remove_task view."""
      response = self.client.get(reverse('remove_task', args=(self.task.id,)))
      self.assertRedirects(response, reverse('task-list'))
      self.assertEqual(Task.objects.count(), 0)


#Unit Tests for urls
class UrlsUnitTest(SimpleTestCase):

  def test_home_url_resolves(self):
    url = reverse('home')
    self.assertEquals(resolve(url).func, home_page)

  def test_calendar_url_resolves(self):
    url = reverse('calendar')
    self.assertEquals(resolve(url).func, calendar)

  def test_calendar_specific_url_resolves(self):
    url = reverse('calendar', args=[2023, 4])
    self.assertEquals(resolve(url).func, calendar)

  def test_prev_month_url_resolves(self):
    url = reverse('prev_month', args=[2023, 3])
    self.assertEquals(resolve(url).func, prev_month_view)

  def test_next_month_url_resolves(self):
    url = reverse('next_month', args=[2023, 5])
    self.assertEquals(resolve(url).func, next_month_view)

  def test_task_list_url_resolves(self):
    url = reverse('task-list')
    self.assertEquals(resolve(url).func.view_class, TaskListView)

  def test_add_task_url_resolves(self):
    url = reverse('add-task')
    self.assertEquals(resolve(url).func, create_task)

  def test_quest_game_url_resolves(self):
    url = reverse('quest-game')
    self.assertEquals(resolve(url).func, start_game)

  def test_complete_task_url_resolves(self):
    url = reverse('complete_task', args=[1])
    self.assertEquals(resolve(url).func, complete_task)

  def test_remove_task_url_resolves(self):
    url = reverse('remove_task', args=[1])
    self.assertEquals(resolve(url).func, remove_task)

# Unit Tests for forms 
class TaskFormUnitTests(TestCase):

  def test_task_form_valid_data(self):
    """Test the TaskForm with valid data."""
    form = TaskForm(data={
        'date': timezone.now().date(),
        'time': timezone.now().time(),
        'name': 'Test Task',
        'difficulty': 3,
        'priority': 2,
        'points': 10
    })
    self.assertTrue(form.is_valid())

  def test_task_form_invalid_data(self):
    """Test the TaskForm with invalid data (e.g., negative points)."""
    form = TaskForm(data={
        'date': timezone.now().date(),
        'time': timezone.now().time(),
        'name': '',
        'difficulty': 3,
        'priority': 2,
        'points': -10  # Invalid due to negative value
    })
    self.assertFalse(form.is_valid())
    self.assertIn('points', form.errors)
    self.assertIn('name', form.errors)

  def test_task_form_missing_data(self):
    """Test the TaskForm with some fields missing."""
    form = TaskForm(data={})
    self.assertFalse(form.is_valid())
    # Check that each field has an error message
    for field in ['date', 'time', 'name', 'difficulty', 'priority', 'points']:
        self.assertIn(field, form.errors)

  def test_task_form_field_labels(self):
    """Test that form fields have correct labels."""
    form = TaskForm()
    self.assertEqual(form.fields['name'].label, "Task Name")
    #self.assertEqual(form.fields['points'].label, "Points")

  def test_task_form_placeholder(self):
    """Test that the 'name' field has the correct placeholder."""
    form = TaskForm()
    self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Task Name')


# Tests User Access to Different Templates of our Page 
class AccessControlUnitTestLoggedOut(TestCase): 
  def setUp(self):
    # Create a user for authentication purposes
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.login_url = reverse('login') 

  def test_access_calendar_without_login(self):
    response = self.client.get(reverse('calendar'))
    self.assertRedirects(response, f'{self.login_url}?next=/calendar/')

  def test_access_create_task_without_login(self):
    response = self.client.get(reverse('add-task'))
    self.assertRedirects(response, f'{self.login_url}?next=/addtask/')

  def test_access_home_page_without_login(self):
    response = self.client.get('/')
    self.assertRedirects(response, f'{self.login_url}?next=/')

  def test_access_remove_task_without_login(self):
    response = self.client.get(reverse('remove_task', args=[1]))
    self.assertRedirects(response, f'{self.login_url}?next=/remove-task/1/')

  def test_access_complete_task_without_login(self):
    response = self.client.get(reverse('complete_task', args=[1]))
    self.assertRedirects(response, f'{self.login_url}?next=/complete-task/1/')

class AccessControlUnitTestsLoggedIn(TestCase): 
  def setUp(self):
      # Create a user for authentication purposes
      self.user = User.objects.create_user(username='testuser', password='12345')
      # Log the user in for subsequent test methods
      self.client.login(username='testuser', password='12345')

  def test_calendar_access_with_login(self):
      response = self.client.get(reverse('calendar'))
      # Expecting a successful response code, such as 200
      self.assertEqual(response.status_code, 200)

  def test_create_task_access_with_login(self):
      # The correct name is 'add-task' based on your urls.py
      response = self.client.get(reverse('add-task'))
      # Expecting a successful response code, such as 200
      self.assertEqual(response.status_code, 200)

  def test_home_page_access_with_login(self):
      # The correct path is just '/' for home_page based on your urls.py
      response = self.client.get('/')
      # Expecting a successful response code, such as 200
      self.assertEqual(response.status_code, 200)

  def test_remove_task_access_with_login(self):
      # Setup: Create a Task to be removed. You'll need a Task ID that exists.
      task = Task.objects.create(name="Test Task", user=self.user, date="2023-01-01", time="12:00", difficulty=1, points=10)
      # Test the remove_task view with a logged-in user
      response = self.client.get(reverse('remove_task', args=[task.id]))
      # Depending on your view, you might expect a redirect after deletion
      self.assertRedirects(response, reverse('task-list'))

  def test_complete_task_access_with_login(self):
      # Setup: Create a Task to be completed.
      task = Task.objects.create(name="Complete Task", user=self.user, date="2023-01-02", time="13:00", difficulty=1, points=20)
      # Test the complete_task view with a logged-in user
      response = self.client.get(reverse('complete_task', args=[task.id]))
      # Depending on your view, you might expect a redirect after completing the task
      self.assertRedirects(response, reverse('task-list'))