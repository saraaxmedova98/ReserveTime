from django.test import TestCase
from account.models import User,Customer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.urls import reverse

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", first_name="test", last_name='test')

    def test_user_str(self):

        self.assertEqual(str(self.user), self.user.email)

class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", first_name="test", last_name='test')
        self.customer = Customer.objects.create(user=self.user)

    def test_check_customer(self):

        self.assertTrue(self.customer)

    def test_customer_str(self):
        
        self.assertEqual(str(self.customer),self.customer.user.email)

class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='12test12')
        self.user.save()

    def tearDown(self):
        self.assertTrue(self.user)
        # self.user.delete()

    # def test_correct(self):
        # user = authenticate(username='test@gmail.com', password='!!!!sara')
        # login(request, user)
        # print(user)
        # self.assertTrue(user.is_authenticated)
        

    # def test_wrong_username(self):
    #     user = authenticate(username='wrong', password='12test12')
    #     self.assertFalse(user is not None and user.is_authenticated)

    # def test_wrong_pssword(self):
    #     user = authenticate(username='test', password='wrong')
    #     self.assertFalse(user is not None and user.is_authenticated)

