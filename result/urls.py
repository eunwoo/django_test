from django.urls import path
from . import views

app_name = "result"

urlpatterns = [path("result/", views.search, name="search")]
