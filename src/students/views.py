from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    success_url = reverse_lazy('students:...')
    form_class = UserCreationForm

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        kwargs_for_authenticate = {
            'request': self.request,
            'username': cd['username'],
            'password': cd['password1'],
        }
        user = authenticate(**kwargs_for_authenticate)
        login(self.request, user)
        return result
