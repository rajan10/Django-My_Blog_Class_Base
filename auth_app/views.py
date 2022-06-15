from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
class RegistrationView(FormView):
    template_name="auth_app/register.html"
    form_class=UserForm
    success_url = '/'

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)


class loginView(FormView):
    template_name="auth_app/login.html"
    form_class=AuthenticationForm

    def form_valid(self, form):
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            self.success_url='/'
        else:
            messages.error(self.request, "invalid username or password")
            self.success_url="auth_app/login"
        return super().form_valid(form)

def logoutView(request):
    logout(request)
    return redirect('/')