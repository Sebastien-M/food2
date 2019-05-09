from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
