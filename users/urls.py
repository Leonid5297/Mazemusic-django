from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("logout/", views.logout, name="logout"),
    path("admin_sign_in/", views.redirect_admin, name="admin_sign_in"),

]
