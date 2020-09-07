from django.test import TestCase
from django.urls import reverse


class CompanyProfileTest(TestCase):

    def test_user_profile_url_name(self):

        response = self.client.get(reverse('account:company-profile', args=(1,)), follow=True)    # for object that doesn't exists
        self.assertEqual(response.status_code, 200)