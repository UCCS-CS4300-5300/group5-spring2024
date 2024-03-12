from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your tests here.
class AccountsTests(TestCase):
  # Create some test data
  def setUp(self):
    # Create a test client
    self.client = Client()
    self.username = 'testUser'
    self.password = 'testPassword!'
    self.user = User.objects.create_user(username=self.username, password=self.password)
                                         
  def test_login_success(self):
    # Perform login request
    response = self.client.post('/accounts/login/', {'username': self.username, 
                                                'password': self.password}, follow=True)
    # Check that the user was logged in successfully
    self.assertEqual(response.status_code, 200)
    self.assertRedirects(response, expected_url='/', status_code=302)

  def test_login_failure(self):
    # Perform login request
    login_failed = self.client.login(username=self.username, password="WrongPassword!")
    # Check that login was not successful
    self.assertFalse(login_failed)

  def test_create_account_success(self):
    username = 'testUser2'
    password = 'testPassword2!'
    # Perform login request
    response = self.client.post('/accounts/signup/', {'username': username, 
                                'password1': password, 'password2': password}, follow=True)

    # Check that the account was created successfully
    self.assertEqual(response.status_code, 200)
    # ensure that the username was created
    self.assertTrue(User.objects.filter(username=username).exists())
    