"""AdaptedMap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required as lr
from django.urls import path, include
from django.views.generic import TemplateView
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
    path('api/user/', include('user.urls')),
    path('api/map/', include('map.urls')),
    path('openapi/',
         get_schema_view(
             title="Adapted Map",
             description="API",
             authentication_classes=[SessionAuthentication],
             permission_classes=[IsAuthenticated],
             renderer_classes=[
                 CamelCaseJSONRenderer,
             ]
         ),
         name='openapi-schema',
         ),

    path('swagger-ui/',
         lr(
             TemplateView.as_view(
                 template_name='swagger-ui.html',
                 extra_context={'schema_url': 'openapi-schema'}
             ),
         ), name='swagger-ui')
]

if settings.DEBUG:
    # -- Static Serving
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
