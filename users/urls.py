from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserDetailView, UserUpdateView, UserDeleteView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path("users/", UserListView.as_view(), name="users_list"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("<str:token>/", UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),

    path("password_reset/", auth_views.PasswordResetView.as_view(), name='password_reset_form'),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
