from django.urls import path
from . import views 

urlpatterns = [
    path("", views.sales , name = "sales"),
    path("get_med_sale", views.get_med_sale , name = "get_med_sale"),
    path("get_med_stock_info", views.get_med_stock_info , name = "get_med_stock_info"),
    path("get_customer", views.get_customer , name = "get_customer"),
    path("get_customer_id", views.get_customer_id , name = "get_customer_id"),
]