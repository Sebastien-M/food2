from django.urls import path
from app.views import IndexView, SignUpView, SignInView, LogoutView, WeekMenuView, DailyRecipeView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('daily-recipe/', DailyRecipeView.as_view(), name='daily-recipe'),
    path('week-menu/', WeekMenuView.as_view(), name='week-menu'),
]
