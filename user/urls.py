from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "user"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/usertype", views.usertype, name="usertype"),
    path("register/agreement_for_user", views.agreeForUser, name="agreeForUser"),
    path("register/agreement_for_admin", views.agreeForAdmin, name="agreeForAdmin"),
    path("register/user", views.registerUser, name="registerUser"),
    path("register/admin", views.registerAdmin, name="registerAdmin"),
    path("editUser/", views.editUser, name="editUser"),
]
