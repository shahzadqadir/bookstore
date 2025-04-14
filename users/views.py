from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib.auth import get_user_model

from users.forms import CustomUserCreationForm

class UserCreationView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


