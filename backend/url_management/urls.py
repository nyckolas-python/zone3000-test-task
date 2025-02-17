from django.urls import path

from .views import RedirectRuleCreateAPI, RedirectRuleManageAPI

urlpatterns = [
    path('', RedirectRuleCreateAPI.as_view(), name='redirect-rule-create'),
    path('<uuid:id>/', RedirectRuleManageAPI.as_view(), name='redirect-rule-manage'),
]
