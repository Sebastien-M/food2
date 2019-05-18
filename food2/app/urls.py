from django.urls import path, re_path
from app.views import IndexView, SignUpView, SignInView, LogoutView, WeekMenuView, TodaysRecipeView, DefineRecipeView, \
    ShoppingListView, ShoppingListItemUpdateView, ShoppingListItemCreateView, ShoppingListItemDeleteView, \
    RecipeDetailView, DailyRecipeDeleteView, ChangeLanguageView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('language/<str:lang>', ChangeLanguageView.as_view(), name='change-language'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('daily-recipe/', TodaysRecipeView.as_view(), name='daily-recipe'),
    path('daily-recipe/delete/<int:pk>/', DailyRecipeDeleteView.as_view(), name='daily-recipe-delete'),
    path('week-menu/', WeekMenuView.as_view(), name='week-menu'),
    path('define-recipe/', DefineRecipeView.as_view(), name='define-recipe'),
    path('shopping_list/', ShoppingListView.as_view(), name='shopping-list'),
    path('shopping_list/update/<int:pk>/', ShoppingListItemUpdateView.as_view(), name='shopping-list-item-update'),
    path('shopping_list/delete/<int:pk>/', ShoppingListItemDeleteView.as_view(), name='shopping-list-item-delete'),
    path('shopping_list/create/', ShoppingListItemCreateView.as_view(), name='shopping-list-item-create'),
    # re_path(r'define-recipe/(?P<date>\d{4}-\d{1,2}-\d{1,2})/$', DefineRecipeView.as_view(), name='define-recipe'),
]
