from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView

from accounts.forms import CustomUserCreationForm, UserProfileForm
from accounts.models import CustomUser

# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Your account was created successfully. You can now log in."


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Your profile was updated successfully."

    def get_object(self, queryset=None):
        return self.request.user