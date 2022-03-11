from django.urls import path
from . import views

app_name = "result"

urlpatterns = [
    path("result/", views.search, name="search"),
    path("search/", views.search_result, name="search_result"),
]
