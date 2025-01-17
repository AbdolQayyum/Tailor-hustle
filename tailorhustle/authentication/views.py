from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import UserForm
from django.contrib.auth import (
    authenticate, login, logout, get_user_model
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

# Create your views here.

User = get_user_model

class SignUpView(View):
    template_name = 'authentication/signup.html'
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin_url')

        payload = {
            'form': form,
        }
        return render(request, self.template_name, payload)


class SignInView(View):
    template_name = 'authentication/signin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        emial_username = request.POST.get('email_username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=emial_username)
            email = user_obj.email
        except Exception as e:
            email = emial_username

        user_ath = authenticate(request, email=email, password=password)

        if user_ath is None:
            messages.error(request, 'Invalid Credentials')
            return render(request, self.template_name)

        login(request, user_ath)
        messages.success(request, 'Login Sucessful')
        return redirect('signin_url')


class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('signin_url')

class PRView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'

class PRDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'

class PRConfirmView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset_confirm.html'

class PRCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'

class PChangeView(PasswordChangeView):
    template_name = 'authentication/password_change.html'
    success_url = reverse_lazy('password_change_done_view')

class PChangeDoneView(PasswordChangeDoneView):
    template_name = 'authentication/password_change_done.html'