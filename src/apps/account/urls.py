from django.urls import path

from apps.account.views import profile, contact_us, index, create_request, cache_test


app_name = 'account'
urlpatterns = [
    path('index/', index, name='index'),
    path('profile/', profile, name = 'profile'),
    path('contact-us/', contact_us),
    path('cache_test/', cache_test, name='cache_test'),
    path('created-request/', create_request, name='create-request'),
]
