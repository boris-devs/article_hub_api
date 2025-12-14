from django.urls import path

from users.views import UserRegisterView, UserLoginView, UserProfileView

urlpatterns = [
    path("auth/register/", UserRegisterView.as_view(), name="register-user"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/profile/", UserProfileView.as_view(), name="profile"),

]
