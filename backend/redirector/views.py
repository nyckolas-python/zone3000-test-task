from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from url_management.models import RedirectRule


@api_view(['GET'])
@permission_classes([AllowAny])
def public_redirect(request, redirect_identifier):
    """
        Public redirects - no authentication required
    """
    rule = get_object_or_404(RedirectRule, redirect_identifier=redirect_identifier, is_private=False)
    return redirect(rule.redirect_url)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def private_redirect(request, redirect_identifier):
    """
        Private redirects - access only for the owner
    """
    rule = get_object_or_404(RedirectRule,
                             redirect_identifier=redirect_identifier,
                             is_private=True,
                             owner=request.user)
    return redirect(rule.redirect_url)
