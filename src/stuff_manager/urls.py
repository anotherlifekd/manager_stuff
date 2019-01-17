from django.contrib import admin
from django.urls import path, include
from apps.account.views import faq, tos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('faq/', faq),
    path('tos/', tos),
    path('account/', include('apps.account.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
