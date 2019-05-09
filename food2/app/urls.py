from django.urls import path, re_path
from app.views import IndexView, SignUpView, SignInView, LogoutView, WeekMenuView, DailyRecipeView, DefineRecipeView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('daily-recipe/', DailyRecipeView.as_view(), name='daily-recipe'),
    path('week-menu/', WeekMenuView.as_view(), name='week-menu'),
    re_path(r'define-recipe/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', DefineRecipeView.as_view(), name='define-recipe'),
]
