from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from apps.account.models import User

@receiver(pre_save, sender=User)
def user_pre_save(sender, *args, **kwargs):
    instance = kwargs['instance']
    if instance.phone:
        instance.phone = ''.join(i for i in instance.phone if i.isdigit())

@receiver(pre_delete, sender=User)
def user_pre_delete(*args, **kwargs):
    raise IntegrityError('Cannot delete user')