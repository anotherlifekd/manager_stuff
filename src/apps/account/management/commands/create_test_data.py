from uuid import uuid4
from django.core.management.base import BaseCommand, CommandError
from apps.account.models import User, City
import random
import names
import string


# generate random emails
domains = ["hotmail.com", "gmail.com", "mail.com" , "mail.ru", "yahoo.com", "yandex.ru", "ukr.net"]
letters = string.ascii_lowercase[:12]

def get_one_random_domain(domains):
    return random.choice(domains)

def get_one_random_name(letters):
    return ''.join(random.choice(letters) for i in range(random.randint(5,12)))

def generate_random_emails():
    return get_one_random_name(letters) + '@' + get_one_random_domain(domains)


# TODO python manage.py create_test_data
# class Command(BaseCommand):
#     help = 'Create test data'
#
#     def handle(self, *args, **options):
#         print('User count', User.objects.count())
#         print('hello from custom command')
#         # User.objects.exclude(is_superuser=True).delete()
#         # for i in range(10_000):
#         #     user = User.objects.create(
#         #         username=str(names.get_full_name() + names.get_full_name()),
#         #         first_name=names.get_first_name(),
#         #         last_name=names.get_last_name(),
#         #         email=generate_random_emails(),
#         #         age=random.randint(18, 60),
#         #         password=get_one_random_name(letters),
#         #     )
#         #     if user1 in User.objects.all():
#         #         continue
#         #     user1 = User.objects.create(
#         #         username=names.get_full_name()
#         #     )

class Command(BaseCommand):
    help = 'Create test data'

    def handle(self, *args, **options):
        # https://pypi.org/project/names/
        User.objects.exclude(is_superuser=True).delete()
        result = []

        cities = []
        for name in ('Kiev', 'Odessa', 'Lviv', 'Dnipro'):
            city, _ = City.objects.get_or_create(name=name)
            cities.append(city)
        for i in range(10_000):
            username = str(uuid4())
            user = User(
                username=username,
                email=username + '@example.com',
                age=random.randint(12, 100),
                salary=random.randint(100, 1000),
                city=random.choice(cities),
            )
            result.append(user)
        User.objects.bulk_create(result)
