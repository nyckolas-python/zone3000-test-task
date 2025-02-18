from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from url_management.models import RedirectRule


def public_redirect(request, redirect_identifier):
    """
    Public redirects - no authentication required
    """
    rule = get_object_or_404(
        RedirectRule, redirect_identifier=redirect_identifier, is_private=False
    )
    return redirect(rule.redirect_url)


@login_required
def private_redirect(request, redirect_identifier):
    """
    Private redirects - access only for the owner
    """
    rule = get_object_or_404(
        RedirectRule, redirect_identifier=redirect_identifier, is_private=True
    )

    if rule.owner != request.user:
        return HttpResponseForbidden(
            "You do not have permission to access this redirect."
        )

    return redirect(rule.redirect_url)
