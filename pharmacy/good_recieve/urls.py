from django.urls import path
from . import views 

urlpatterns = [
    path("members", views.members),
    path("", views.good_recieved , name = "gr_home"),
    path("get_med", views.get_med , name = "get_med"),
    path("get_med_price", views.get_med_price , name = "get_med_price"),
    path("save_requisition", views.save_requisition , name = "save_requisition"),
    path("get_ordered", views.get_ordered , name = "get_ordered"),
    path("insert_inventory", views.insert_inventory , name = "insert_inventory"),
    path("logout", views.logout , name = "logout"),
    path("gr_filter", views.gr_filter , name = "gr_filter"),
    path("rePdf", views.rePdf , name = "rePdf"),
    path("edit_requisition", views.edit_requisition , name = "edit_requisition"),
]