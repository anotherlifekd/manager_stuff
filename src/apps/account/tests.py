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
                                     'from_date': datetime(2020, 1, 2),
                                     'to_date': datetime(2020, 1, 1),
                                     'status_changed': datetime(2020, 1, 1)})
        self.assertEqual(response.context['form'].errors['to_date'],
                         ['from_date cannot be greater then to_date'])

        response = client.post(reverse('account:create-request'),
                               data={'type': mch.REQUEST_DAYOFF,
                                     'from_date': datetime(2020, 1, 2),
                                     'to_date': datetime(2020, 1, 15),
                                     'status_changed': datetime(2020, 1, 2)})
        self.assertEqual(response.context['form'].errors['to_date'],
                         ['dayoff should be not more then 1 day'])

        response = client.post(reverse('account:create-request'),
                               data={'type': mch.REQUEST_VACATION,
                                     'from_date': datetime(2018, 12, 19),
                                     'to_date': datetime(2019, 2, 10),
                                     'status_changed': datetime(2019, 1, 29)})
        self.assertEqual(response.context['form'].errors['to_date'],
                         ['vocation 20 days'])

        response = client.post(reverse('account:create-request'),
                               data={'type': mch.REQUEST_VACATION,
                                     'from_date': datetime(2018, 12, 19),
                                     'to_date': datetime(2019, 1, 5),
                                     'status_changed': datetime(2019, 1, 29)})
        self.assertEqual(response.context['form'].errors['type'],
                         ["you have not enough days to get this vacation"])

    def test_other_form(self):
        pass