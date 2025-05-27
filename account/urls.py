from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.LoginView.as_view(),name="login"),
    path("logout/", views.LogoutUser,name="logout"),
    path("register/", views.RegisterView.as_view(),name="register"),
    path("checkotp/", views.OtpCheckView.as_view(),name="checkotp"),
]