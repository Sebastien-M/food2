import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from app.forms import SignUpForm, SignInForm
from app.models import DailyRecipe


class IndexView(TemplateView):
    template_name = "app/index.html"


class SignUpView(FormView):
    template_name = "app/pages/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        try:
            User.objects.create_user(first_name=cleaned_data['first_name'],
                                     last_name=cleaned_data['last_name'],
                                     email=cleaned_data['email'],
                                     password=cleaned_data['password'],
                                     username=cleaned_data['username'])
        except IntegrityError:
            form.add_error(error="Nom d'utilisateur déjà existant", field="username")
            return super(SignUpView, self).form_invalid(form)
        return super().form_valid(form)


class SignInView(FormView):
    template_name = "app/pages/signin.html"
    form_class = SignInForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            form.add_error(error="Nom d'utilisateur ou mot de passe incorect", field="username")
            form.add_error(error="Nom d'utilisateur ou mot de passe incorect", field="password")
            return super(SignInView, self).form_invalid(form)
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


class WeekMenuView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('signin')
    template_name = "app/pages/week_menu.html"

    def get_context_data(self, **kwargs):
        context = super(WeekMenuView, self).get_context_data(**kwargs)
        return context


class DailyRecipeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('signin')
    template_name = "app/pages/daily_recipe.html"

    def get_context_data(self, **kwargs):
        context = super(DailyRecipeView, self).get_context_data(**kwargs)
        todays_date = datetime.date.today()
        try:
            daily_recipe = DailyRecipe.objects.get(user=self.request.user, day=todays_date)
            todays_recipe = daily_recipe.recipe
            context['todays_recipe'] = todays_recipe
        except DailyRecipe.DoesNotExist:
            context['todays_recipe'] = None
        return context
