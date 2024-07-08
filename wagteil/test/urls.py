"""
URL configuration for test project.

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
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import path, include, reverse
from django.contrib import admin
from django.utils.http import url_has_allowed_host_and_scheme
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from users.urls import urlpatterns as users_urls
from django.conf import settings
from django.conf.urls.static import static
from info.urls import api_router
from users.views import LoginViewCustom


urlpatterns = [
    path('admin/', admin.site.urls),
    path("cms/login/", LoginViewCustom.as_view(), name="wagtailadmin_login"),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('api/v2/', api_router.urls),
    # Важно, чтобы обращение к API было раньше, чем wagtail_urls
    path(r'', include(wagtail_urls)),
    path(r'', include(users_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

