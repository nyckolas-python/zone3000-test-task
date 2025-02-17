from django.contrib import admin

from .models import RedirectRule


@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = ('redirect_identifier', 'redirect_url', 'is_private', 'created', 'modified')
    readonly_fields = ('id', 'created', 'modified', 'redirect_identifier')
    search_fields = ('redirect_identifier', 'redirect_url')
    list_filter = ('is_private', 'created', 'modified')
