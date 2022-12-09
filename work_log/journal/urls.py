from django.urls import path
from .journal import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("/lists/new_url/", views.view_list, name="view_list"),
]
