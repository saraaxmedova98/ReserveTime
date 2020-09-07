from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get(reverse('core:home'), follow=True)
        self.assertEquals(response.status_code , 200)

        self.assertTemplateUsed(response, 'home-page.html')

class UserProfileTest(TestCase):
    def test_user_profile_url_name(self):

        response = self.client.get(reverse('account:user-profile', args=(1,)), follow=True)    # for object that doesn't exists
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'user-profile.html')

 