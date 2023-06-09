"""PaperFives URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from PaperFives.settings import MEDIA_ROOT, MEDIA_URL
from zeta.views.not_found import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pseudo/', include(('pseudo.urls', 'pseudo'))),
    path('api/v1/users/', include(('users.urls', 'users'))),
    path('api/v1/papers/', include(('papers.urls', 'papers'))),
    path('api/v1/msgs/', include(('msgs.urls', 'msgs'))),
    path('api/v1/zeta/', include(('zeta.urls', 'zeta'))),
    # re_path(r'^search/', include('haystack.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

# only be used when Debug is false
urls.handler404 = page_not_found
