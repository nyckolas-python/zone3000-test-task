from django.urls import path

from .views import UserCreateAPI, UserManageAPI

urlpatterns = [
    path('', UserCreateAPI.as_view(), name='user-create'),
    path('<int:pk>/', UserManageAPI.as_view(), name='user-manage'),
]