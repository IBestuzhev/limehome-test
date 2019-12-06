"""apistored URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

from django.views.static import serve

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


api_urls = [  # Keep it separate so Swagger Gen does not look into non-API urls
    path('api/', include('hotels.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += api_urls

if settings.ENABLE_SWAGGER:
    schema_view = get_schema_view(
        openapi.Info(
            title="Hotel Lookup API",
            default_version='v1',
            description='Limehome Coding challenge. '
                        'https://gitlab.com/limehome/interviews/coding-challenge',
            contact=openapi.Contact(email='best.igor@gmail.com'),
        ),
        public=True,
        patterns=api_urls
    )

    urlpatterns += [
        re_path(r'^api/doc(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^api/doc/$', schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'),
        re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'),
    ]


urlpatterns += [  # Add them last and this is cathc all URL
    path('', serve, dict(document_root=settings.REACT_BUILD_PATH, path='index.html')),
    path('<path:path>', serve, dict(document_root=settings.REACT_BUILD_PATH, show_indexes=True))
]
