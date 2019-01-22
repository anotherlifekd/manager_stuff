from django.contrib import admin
from apps.account.models import User, City, ContactUs, RequestDayOffs
from apps.account.forms import UserAdminForm
from apps import model_choices as mch

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ['id', 'username', 'email', 'age']
    list_filter = ['date_joined', 'last_login', 'age']
    list_per_page = 10
    search_fields = ['email', 'first_name', 'phone']

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['last_login', 'date_joined', 'phone', 'username']
        return []

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return UserAdminForm
        else:
            return super().get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return not obj.is_superuser
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = [
        'title', 'email', 'text',
    ]


@admin.register(RequestDayOffs)
class RequestDayOffsAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'type']
    list_display = ["user", "from_date", "to_date", "reason", "type"]
    search_fields = ["user", "from_date", "to_date", "reason", "type"]
    list_filter = ["status", 'type']

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['user']
        if obj.status != mch.STATUS_PENDING:
            return ["status"]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.group.name:
    #         return qs.exclude(name='test')