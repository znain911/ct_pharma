from django.urls import path
from . import views 

urlpatterns = [
    #path("members", views.members),
    path("", views.main , name = "in_home"),
    path("get_inventry_day", views.get_inventry_day , name = "get_inventry_day"),
    path("get_inventry_med", views.get_inventry_med , name = "get_inventry_med"),
    path("get_inventry_all_item", views.get_inventry_all_item , name = "get_inventry_all_item"),
    path("get_traoutletl_list", views.get_traoutletl_list , name = "get_traoutletl_list"),
    path("transfer", views.transfer , name = "transfer"),
]