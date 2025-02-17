from django.contrib.auth.models import User
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.response import Response

from .permissions import IsAdminUser
from .serializers import UserCreateSerializer, UserSerializer

__all__ = ["UserCreateAPI", "UserManageAPI"]


@extend_schema(tags=["users"])
class UserCreateAPI(generics.CreateAPIView):
    """API for creating new users"""

    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserCreateSerializer

    @extend_schema(
        summary="Create a user",
        description="Create a new user. Available only to admin users.",
        request=UserCreateSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Not an admin user"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["users"])
class UserManageAPI(generics.UpdateAPIView, generics.DestroyAPIView):
    """API for updating and deleting users"""

    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return UserCreateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(UserSerializer(instance).data)

    @extend_schema(
        summary="Update a user",
        description="Fully update a user's information. Available only to admin users.",
        request=UserCreateSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Not an admin user"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a user",
        description="Partially update a user's information. Available only to admin users.",
        request=UserCreateSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Not an admin user"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a user",
        description="Delete a user. Available only to admin users.",
        responses={
            204: OpenApiResponse(description="Successfully deleted"),
            403: OpenApiResponse(description="Not an admin user"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
