from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render, HttpResponse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to the login page after successful signup
    template_name = 'registration/signup.html'

class LogoutView(generic.CreateView):
    template_name = 'registration/logout.html'

def profile(request):
    return render(request, 'profile.html')