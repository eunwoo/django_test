from django.urls import path
from . import views

app_name = "announcement"

urlpatterns = [
    path("create/", views.create_views, name="create_announcement"),
]
