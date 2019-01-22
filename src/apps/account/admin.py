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
class RequestDayOffAdmin(admin.ModelAdmin):
    list_filter = ('status', 'type')
    readonly_fields = ('user', 'type')
    # TODO add form
    # TODO subtract dayoffs or vacations on Form Approve

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(self, request)
        if obj is not None:
            # if request.user.is_hr:  # check if request user in group
            # if obj.status != mch.STATUS_PENDING and not request.user.is_superuser:  # allow superuser to change status field
            if obj.status != mch.STATUS_PENDING:
                readonly_fields += ('status', )
                # readonly_fields = readonly_fields + ('status', )
        return readonly_fields