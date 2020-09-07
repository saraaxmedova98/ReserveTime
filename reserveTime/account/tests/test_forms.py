from django.test import TestCase
from django.urls import reverse
from account.models import User
from account.forms import CustomerRegisterForm
class TestRegisterCustomerForm(TestCase):
    def test_story_forms(self):
       
        # category = User.objects.create(
        #     title='Category title'
        #     )
        valid_data = {
            'first_name': 'Sara',
            'last_name': 'Axmedova',
            'username': 'test@gmail.com',
            'password1': 'test12345',
            'password2' : 'test12345'
            }

        form = CustomerRegisterForm(data=valid_data)
        self.assertFalse(form.errors)

        invalid_data = {
            'first_name': 'Sara',
            'last_name': 'Axmedova',
            'username': 'test',
            'password1': 'test123',
            'password2' : 'test12'
            }
        form = CustomerRegisterForm(data=invalid_data)
        self.assertTrue(form.errors)


class TestLoginCustomer(TestCase):
    def test_login(self):
        user = self.client.login(username='tes@gml.com', password='barbaz')
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login-user.html')