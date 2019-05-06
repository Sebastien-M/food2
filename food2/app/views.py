from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView

from app.forms import CreateAccountForm


class IndexView(TemplateView):
    template_name = "app/index.html"


class CreateAccountView(FormView):
    template_name = "app/pages/create_account.html"
    form_class = CreateAccountForm
    success_url = '/'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        User.objects.create_user(first_name=cleaned_data['first_name'],
                                 last_name=cleaned_data['last_name'],
                                 email=cleaned_data['email'],
                                 password=cleaned_data['password'],
                                 username=cleaned_data['username'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
