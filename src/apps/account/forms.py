from django import forms
from apps.account.models import User, ContactUs, RequestDayOffs
from django.db.models import Q
from datetime import timedelta, date, datetime
from apps import model_choices as mch
from apps.account.tasks import send_email_async

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'age', 'email',
            'first_name', 'last_name',
            'city'
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = [
            'title', 'email',
            'text',
        ]

class RequestDayOffForm(forms.ModelForm):
    class Meta:
        model = RequestDayOffs
        fields = [
            'type', 'from_date', 'to_date', 'status_changed'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['from_date'] > cleaned_data['to_date']:
                self.add_error('to_date', 'from_date cannot be greater then to_date')

            data = cleaned_data['to_date'] - cleaned_data['from_date']
            if cleaned_data['type'] == mch.REQUEST_DAYOFF and data.days > 1:
                self.add_error('to_date', 'dayoff should be not more then 1 day')

            if cleaned_data['type'] == mch.REQUEST_VACATION:
                def daterange(start_date, end_date):
                    for n in range(int((end_date - start_date).days)):
                        yield start_date + timedelta(n)

                start_date = cleaned_data['from_date']
                end_date = cleaned_data['to_date']
                count = 0
                for single_date in daterange(start_date, end_date):
                    if single_date.isoweekday() == 6 or single_date.isoweekday() == 7:
                        continue
                    count += 1
                if count > 20:
                    self.add_error('to_date', 'vocation 20 days')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
            # if count > self.user.vacations_days:
            #     self.add_error('type', "you have not enough days to get this vacation ")



class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'age', 'password',
            'email', 'salary'
        ]

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if not self.errors:
            if User.objects.filter(Q(email=cleaned_data['email']) |
                                   Q(username=cleaned_data['email'])).exists():
                print('YES')
                raise forms.ValidationError('User already exists')
        return cleaned_data


class RequestDayOffAdminForm(forms.ModelForm):

    class Meta:
        model = RequestDayOffs
        fields = [
            'created', 'from_date', 'to_date',
            'reason', 'type', 'status', 'status_changed'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['type'] == mch.STATUS_REJECTED:
                if not cleaned_data['reason']:
                    self.add_error('reason', "reason field is required")
            return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = super().clean()
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        start_date = instance.from_date
        end_date = instance.to_date
        count = 0
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == 6 or single_date.isoweekday() == 7:
                continue
            count += 1
        user = User.objects.get(id=instance.user.id)
        days = user.vacations_days - count
        user.vacations_days = days
        if cleaned_data['status'] == mch.STATUS_CONFIRMED:
            instance.status_changed = datetime.now()
            send_email_async.delay(
                'Request Status',
                'Your request has been confirmed',
                user=user.id,
                from_email='bobertestdjango@gmail.com',
                recipient_list=[user.email],
            )
        elif cleaned_data['status'] == mch.STATUS_REJECTED:
            instance.status_changed = datetime.now()
            send_email_async.delay(
                'Request Status',
                'Your request has been rejected',
                user=user.id,
                from_email='bobertestdjango@gmail.com',
                recipient_list=[user.email],
            )
        user.save()

        if commit:
            instance.save()
        return instance


class RequestDayOffAdminAddForm(forms.ModelForm):

    class Meta:
        model = RequestDayOffs
        fields = [
            'created', 'from_date', 'to_date',
            'reason', 'type', 'user'
        ]