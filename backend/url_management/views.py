from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import RedirectRule
from .permissions import IsOwnerOrReadOnly
from .serializers import RedirectRuleSerializer

__all__ = ["RedirectRuleCreateAPI", "RedirectRuleManageAPI"]


@extend_schema(tags=["urls"])
class RedirectRuleCreateAPI(generics.CreateAPIView):
    """API for creating new redirect rules"""

    permission_classes = [IsAuthenticated]
    serializer_class = RedirectRuleSerializer

    @extend_schema(
        summary="Create a redirect rule",
        description="Create a new redirect rule for the current user.",
        request=RedirectRuleSerializer,
        responses={
            201: RedirectRuleSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Sets the owner of the redirect rule to the current user"""
        serializer.save(owner=self.request.user)


@extend_schema(tags=["urls"])
class RedirectRuleManageAPI(generics.UpdateAPIView, generics.DestroyAPIView):
    """API for updating and deleting specific redirect rules"""

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = RedirectRuleSerializer
    lookup_field = 'id'

    @extend_schema(
        summary="Update a redirect rule",
        description="Fully update a redirect rule. Available only to the owner.",
        request=RedirectRuleSerializer,
        responses={
            200: RedirectRuleSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Not the owner"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a redirect rule",
        description="Partially update a redirect rule. Available only to the owner.",
        request=RedirectRuleSerializer,
        responses={
            200: RedirectRuleSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Not the owner"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a redirect rule",
        description="Delete a redirect rule. Available only to the owner.",
        responses={
            204: OpenApiResponse(description="Successfully deleted"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Not the owner"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return RedirectRule.objects.all()
