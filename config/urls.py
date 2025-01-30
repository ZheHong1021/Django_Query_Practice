"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from config.django.base import DEBUG
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import api_404_handler


# All
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.system.user.urls')),
    path("api/", include('apps.system.group.urls')),
    path("api/", include('apps.system.permission.urls')),
    path('api/', include('apps.auth.jwt_token.urls')),
    path('api/', include('apps.posts.urls')),


    # Swagger-UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    
    re_path(r'^api/.*$', api_404_handler),
]



# Development Mode
if DEBUG:

    urlpatterns += [
        # debug_toolbar
        path("__debug__/", include(debug_toolbar.urls)),
        
    ]

    # Static and Media
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Production Mode
else:
    urlpatterns += [

    ]
