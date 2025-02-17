from django.urls import path

from .views import private_redirect, public_redirect

urlpatterns = [
    path('public/<str:redirect_identifier>/', public_redirect, name='public-redirect'),
    path('private/<str:redirect_identifier>/', private_redirect, name='private-redirect'),
]
