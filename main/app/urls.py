from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginPage.as_view()),
    path("logout/", views.Logout.as_view()),
    path("create_new_user_fallback/", views.CreateNewUserFallback.as_view()),
    path("user/details/", views.UserDetails.as_view()),
]
