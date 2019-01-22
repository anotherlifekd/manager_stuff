from celery import shared_task
from django.core.mail import send_mail


@shared_task
def task_number_one():
    from time import sleep
    sleep(10)
    print('Hello from number One')


@shared_task
def increment_dayoffs():
    from apps.account.models import User

    for user in User.objects.all().iterator():
        # TODO
        try:
            user.sickness_days += 2
            user.vacation_days += 2
            user.save()
            # send_email_async.delay(user)
        except Exception:
            pass


@shared_task
def send_email_async(*args, **kwargs):
    from apps.account.models import User

    user_id = kwargs.pop('user')
    user = User.objects.get(id=user_id)

    send_mail(*args, **kwargs)
        # subject='Subject here',
        # message='Here is the message.',
        # from_email='from@example.com',
        # recipient_list=['to@example.com'],
        # fail_silently=False,
    # )