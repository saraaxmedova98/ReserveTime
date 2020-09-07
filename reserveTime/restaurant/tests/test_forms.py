from django.test import TestCase
from django.urls import reverse
from account.models import User
from account.forms import RestaurantRegisterForm
class TestRegisterCompanyForm(TestCase):
    def test_story_forms(self):
       
        
        valid_data = {
            'first_name': 'Sara',
            'last_name': 'Axmedova',
            'username': 'test@gmail.com',
            'password1': 'test12345',
            'password2' : 'test12345',
            'company_name' : 'Test',
            'phone_number' : '12345',
            'city_location' : 'Baku',
            'province_location' : 'Qusar',
            'country_location' : 'Azerbaijan'
            }

        form = RestaurantRegisterForm(data=valid_data)
        self.assertFalse(form.errors)

        invalid_data = {
            'first_name': 'Sara',
            'last_name': 'Axmedova',
            'username': 'test@gmail.com',
            'password1': 'test12345',
            'password2' : 'test1245',
            'phone_number' : '12345',
            'city_location' : 'Baku',
            'province_location' : 'Qusar',
            'country_location' : 'Azerbaijan'
            }
        form = RestaurantRegisterForm(data=invalid_data)
        self.assertTrue(form.errors)

