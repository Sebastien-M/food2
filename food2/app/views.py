import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import translation
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, UpdateView, CreateView, DeleteView, DetailView
from django.utils.translation import gettext as _

from app.forms import SignUpForm, SignInForm, DefineRecipeForm
from app.models import Recipe, DailyRecipe, IngredientRecipe, ShoppingListItem
from app.utils import is_daily_recipe_defined_for_user, get_todays_recipe_for_user, format_recipe_steps, \
    get_this_week_menu, str_to_date
from food2.settings import LANGUAGES


class IndexView(TemplateView):
    template_name = "app/index.html"


class SignUpView(FormView):
    template_name = "app/pages/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        try:
            User.objects.create_user(first_name=cleaned_data["first_name"],
                                     last_name=cleaned_data["last_name"],
                                     email=cleaned_data["email"],
                                     password=cleaned_data["password"],
                                     username=cleaned_data["username"])
        except IntegrityError:
            form.add_error(error=_("Nom d'utilisateur déjà existant"), field="username")
            return super(SignUpView, self).form_invalid(form)
        return super().form_valid(form)


class SignInView(FormView):
    template_name = "app/pages/signin.html"
    form_class = SignInForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            form.add_error(error=_("Nom d'utilisateur ou mot de passe incorect"), field="username")
            form.add_error(error=_("Nom d'utilisateur ou mot de passe incorect"), field="password")
            return super(SignInView, self).form_invalid(form)
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("index"))


class WeekMenuView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("signin")
    template_name = "app/pages/week_menu.html"

    def get_context_data(self, **kwargs):
        context = super(WeekMenuView, self).get_context_data(**kwargs)
        week_menu = get_this_week_menu(self.request.user)
        context["week_menu"] = week_menu
        return context

    def get_week_menu_for_user(self, user):
        pass


class TodaysRecipeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("signin")
    template_name = "app/pages/daily_recipe.html"

    def get_context_data(self, **kwargs):
        context = super(TodaysRecipeView, self).get_context_data(**kwargs)
        context["todays_recipe"] = None
        context['todays_date'] = datetime.date.today().strftime('%Y-%m-%d')
        if is_daily_recipe_defined_for_user(self.request.user):
            todays_recipe = get_todays_recipe_for_user(self.request.user)
            recipe_details = todays_recipe.ingredient_quantity.all()
            context["todays_recipe"] = get_todays_recipe_for_user(self.request.user)
            context["recipe_details"] = recipe_details
            context["recipe_steps"] = format_recipe_steps(todays_recipe)
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("signin")
    model = Recipe
    template_name = 'app/pages/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        recipe_details = context['object'].ingredient_quantity.all()
        context["recipe_details"] = recipe_details
        context["recipe_steps"] = format_recipe_steps(context['object'])
        return context


class DefineRecipeView(LoginRequiredMixin, FormView):
    template_name = "app/pages/define_recipe.html"
    form_class = DefineRecipeForm
    login_url = reverse_lazy("signin")
    success_url = reverse_lazy("week-menu")

    def get_context_data(self, **kwargs):
        context = super(DefineRecipeView, self).get_context_data(**kwargs)
        context['random_recipe'] = Recipe.get_random_recipe()
        context['date'] = self.request.GET.get('date')
        return context

    def form_valid(self, form):
        form_valid = super(DefineRecipeView, self).form_valid(form)
        date = str_to_date(form.cleaned_data.get('date'))
        recipe_id = form.cleaned_data.get('recipe')
        choosen_recipe = Recipe.objects.get(id=recipe_id)
        ingredients_recipe = IngredientRecipe.objects.filter(recipe=choosen_recipe)
        user = self.request.user

        for ingredient_recipe in ingredients_recipe:
            item_already_in_list = ShoppingListItem.objects.filter(user=user,
                                                                   ingredient=ingredient_recipe.ingredient.name).exists()
            if item_already_in_list and ingredient_recipe.quantity:
                list_item = ShoppingListItem.objects.get(user=user,
                                                         ingredient=ingredient_recipe.ingredient.name)
                list_item.quantity = float(list_item.quantity) + float(ingredient_recipe.quantity)
                list_item.save()
            elif item_already_in_list:
                continue
            else:
                ShoppingListItem.objects.create(user=self.request.user,
                                                ingredient=ingredient_recipe.ingredient.name,
                                                quantity=ingredient_recipe.quantity)
        daily_recipe = DailyRecipe.objects.filter(user=user, day=date)
        if daily_recipe.exists():
            updated_daily_recipe = daily_recipe.get()
            updated_daily_recipe.recipe = choosen_recipe
            updated_daily_recipe.save()
        else:
            DailyRecipe.objects.create(day=date, recipe=choosen_recipe, user=user)
        return form_valid


class ShoppingListView(LoginRequiredMixin, ListView):
    model = ShoppingListItem
    template_name = 'app/pages/shopping_list.html'
    login_url = reverse_lazy("signin")

    def get_queryset(self):
        items = ShoppingListItem.objects.filter(user=self.request.user)
        duplicate_free_items = []
        for item in items:
            if item not in duplicate_free_items:
                duplicate_free_items.append(item)
        return duplicate_free_items


class ShoppingListItemUpdateView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('shopping-list')
    model = ShoppingListItem
    fields = ['ingredient', 'quantity', 'bought']
    template_name = 'app/pages/shopping_list_item_update_form.html'
    login_url = reverse_lazy("signin")


class ShoppingListItemCreateView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('shopping-list')
    model = ShoppingListItem
    fields = ['ingredient', 'quantity', 'bought']
    template_name = 'app/pages/shopping_list_item_create_form.html'
    login_url = reverse_lazy("signin")

    def form_valid(self, form):
        form.cleaned_data['user_id'] = self.request.user.id
        cleaned_data = form.cleaned_data
        ShoppingListItem.objects.create(**cleaned_data)
        return HttpResponseRedirect(reverse_lazy('shopping-list'))


class ShoppingListItemDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('shopping-list')
    model = ShoppingListItem
    login_url = reverse_lazy("signin")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DailyRecipeDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('signin')
    model = DailyRecipe
    success_url = reverse_lazy('week-menu')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        daily_recipe = self.get_object()
        ingredients_recipe = IngredientRecipe.objects.filter(recipe=daily_recipe.recipe)
        user = self.request.user
        shopping_list = ShoppingListItem.objects.filter(user=user)
        for ingredient_recipe in ingredients_recipe:
            ingredient = ingredient_recipe.ingredient
            new_quantity = ingredient_recipe.quantity
            item_to_modify = shopping_list.filter(ingredient=ingredient)
            if item_to_modify.exists():
                # Only one instance of the ingredient in shopping list
                item_to_modify = item_to_modify.get()
                if item_to_modify.quantity is None:
                    item_to_modify.delete()
                elif float(item_to_modify.quantity) - new_quantity == 0:
                    item_to_modify.delete()
                else:
                    item_to_modify.quantity = float(item_to_modify.quantity) - new_quantity
                    item_to_modify.save()
        return super(DailyRecipeDeleteView, self).delete(request, *args, **kwargs)


class ChangeLanguageView(View):

    def get(self, request, *args, **kwargs):
        user_language = kwargs.get('lang')
        # TODO: use enum for languages
        if user_language in [lang[0] for lang in LANGUAGES]:
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return redirect(reverse_lazy('week-menu'))
