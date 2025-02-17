from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

admin.site.index_title = "ZONE3000-Project Admin Panel"
admin.site.site_header = "ZONE3000-Project Admin Panel"
admin.site.site_title = "ZONE3000-Project Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI endpoints:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # API endpoints
    # path(
    #     "api/v1/", include(
    #         [
                path('retrieve-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                # path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
                path('users', include('users.urls')),
                # better to use "urls" instead of "url"
                path('url/', include('url_management.urls')),
                # path('urls/', include('url_management.urls')),
    #         ],
    #     ),
    # ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += list(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    )
