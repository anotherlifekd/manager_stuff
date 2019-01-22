from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from apps import model_choices as mch


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)  # TODO validate age >= 18
    phone = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    city = models.ForeignKey('account.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    vacations_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    sickness_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0)

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
        # instance = super().save(commit=False)
        # instance.username = instance.email
        #
        # if commit:
        #     instance.save()
        # return instance

class City(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'

class ContactUs(models.Model):
    email = models.EmailField('email address')
    title = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Contact-us'

# class RequestDayOffs(models.Model):
#     from_date = models.DateField(("From date"), default=date.today)
#     to_date = models.DateField(("To date"), default=date.today)
#     REASON_CHOICES = (
#         ('Vacation', 'Vacation'),
#         ('Disease', 'Disease'),
#         ('At own expense', 'At own expense'),
#     )
#     LOCATOR_YES_NO_CHOICES = ((None, ''), (True, 'Confirmed'), (False, 'Rejected'))
#     confirmed = models.NullBooleanField(choices=LOCATOR_YES_NO_CHOICES,
#                                 max_length=3,
#                                 blank=True, null=True, default=None,)
#     reason = models.CharField(max_length=20, choices=REASON_CHOICES)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dayoffs')
#
#     class Meta:
#         verbose_name_plural = 'Request day offs'

class RequestDayOffs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dayoffs')
    created = models.DateTimeField(default=datetime.now)  # auto_now_add
    from_date = models.DateTimeField(null=False, blank=False)
    to_date = models.DateTimeField(null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        null=False, blank=False,
        choices=mch.REQUEST_TYPES,
        default=mch.REQUEST_SICKNESS,
    )
    reason = models.CharField(max_length=256, null=True, blank=True, default=None)  # reason required when status = REJECTED
    status = models.PositiveSmallIntegerField(
        null=False, blank=False,
        choices=mch.STATUSES,
        default=mch.STATUS_PENDING,
    )

    class Meta:
        verbose_name_plural = 'Request day offs'

    def __str__(self):
        return f'status: {self.get_status_display()}'