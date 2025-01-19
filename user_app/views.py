from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from library_app.models import BookBorrowing
from user_app.forms import UserRegistrationForm, UserUpdateForm


class UserRegistrationView(FormView):
    template_name = 'user-registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'user-login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserLMSAccountUpdateView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        borrowed_books = BookBorrowing.objects.filter(borrower=self.request.user)
        return render(request, self.template_name, {'form': form, 'borrowed_books': borrowed_books})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
