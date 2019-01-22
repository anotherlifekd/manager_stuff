from celery import shared_task
from django.core.mail import send_mail

@shared_task
def task_number_one():
    print('Hello from number One')

@shared_task
def send_email_async(*args, **kwargs):
    send_mail(*args, **kwargs)