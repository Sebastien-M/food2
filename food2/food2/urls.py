from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('food2/admin/', admin.site.urls),
    path('food2', include("app.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
