import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserForm, UserRegisterForm
from users.models import User


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users_list.html"
    ordering = ["id"]
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="managers").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        managers_group = Group.objects.get(name="managers")
        filtered_users = User.objects.exclude(is_superuser=True).exclude(groups=managers_group)
        return filtered_users


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "user_detail"

    def get_object(self):
        token = self.kwargs.get("token")
        return get_object_or_404(User, token=token)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "user_form.html"
    success_url = reverse_lazy("mailings:dashboard")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "user_confirm_delete.html"
    success_url = reverse_lazy("mailings:dashboard")


def block_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    messages.success(request, "Пользователь успешно заблокирован.")
    return redirect("users:users_list")
