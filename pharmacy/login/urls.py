from django.urls import path
from . import views 

urlpatterns = [
    path("", views.login , name = "login"),
    path("verify_user/", views.verify_user , name = "verify_user"),
    path("registration", views.registration , name = "registration"),
    path("update_user", views.update_user , name = "update_user"),
    path("register_user", views.register_user , name = "register_user"),
    path("verify_otp", views.verify_otp , name = "verify_otp"),
]