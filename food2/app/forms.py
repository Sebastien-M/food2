from django import forms


class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class DefineRecipeForm(forms.Form):
    recipe = forms.CharField()
    date = forms.CharField()
