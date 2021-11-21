from django.urls import path, re_path

from . import views

app_name = "administration"

urlpatterns = [
    re_path(r"^change_my_password/$", views.change_my_password, name="administrataion_change_my_password"),
]
