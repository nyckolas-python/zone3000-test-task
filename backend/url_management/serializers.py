from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from .models import RedirectRule


class RedirectRuleSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    redirect_identifier = serializers.CharField(read_only=True)

    class Meta:
        model = RedirectRule
        # List of fields; the owner field is considered read-only
        fields = [
            'id',
            'created',
            'modified',
            'redirect_url',
            'is_private',
            'redirect_identifier',
        ]
        read_only_fields = ['id', 'created', 'modified', 'redirect_identifier']

    def validate_redirect_url(self, value):
        """Validate that redirect_url is a proper URL"""
        validator = URLValidator()
        try:
            validator(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid URL format")
        return value
