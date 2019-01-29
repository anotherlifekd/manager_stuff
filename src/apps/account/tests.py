from django.test import TestCase
from datetime import datetime

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse

from apps.account.forms import RequestDayOffForm
from apps.account.models import User
from apps import model_choices as mch

# setUpModuleModule
# tearDownModule


class ViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        print('SetupClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):  # runs before each test
        print('SetUp')
        self.user = User.objects.create(salary=123, email='test@mail.com')
        self.user.set_password('123456')
        self.user.save()

    def tearDown(self):
        print('TearDown')
        # User.objects.filter(email='test@mail.com').delete()

    def test_create_request(self):
        user = self.user

        client = Client()
        response = client.get(reverse('account:create-request'))
        self.assertEqual(response.status_code, 302)  # user is not login

        self.assertTrue(client.login(username=user.username, password='123456'))
        response = client.get(reverse('account:create-request'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('account/create-request.html' in [template.name for template in response.templates])
        self.assertEqual(type(response.context['form']), RequestDayOffForm)
        response = client.post(reverse('account:create-request'),
                               data={'type': mch.REQUEST_DAYOFF,
                                     'date_from': datetime(2020, 1, 2),
                                     'date_to': datetime(2020, 1, 1)})
        self.assertEqual(response.context['form'].errors['date_to'],
                         ['date_from cannot be greater than date_to'])

    def test_other_form(self):
        pass