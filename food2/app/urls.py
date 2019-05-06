from django.urls import path
from app.views import IndexView, CreateAccountView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_account/', CreateAccountView.as_view(), name='create-account')
]