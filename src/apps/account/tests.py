from django.urls import reverse
from django.test import TestCase, Client
from apps.account.models import User

class ViewsTest(TestCase):
    def test_create_request(self):
        user = User.objects.create(salary=123, username='test', email='test@mail.com')
        user.set_password('123456')
        user.save()
        client = Client()
        response = client.get(reverse('account:create-request'))
        self.assertEqual(response.status_code, 302) # user is not login