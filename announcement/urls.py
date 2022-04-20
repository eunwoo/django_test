from django.urls import path
from . import views

app_name = "announcement"

urlpatterns = [
    path("create/", views.create_views, name="create_announcement"),
    path("update/<int:pk>/", views.update_views, name="update_announcement"),
    path("read/<int:pk>/", views.read_views, name="read_announcement"),
    path("delete/", views.delete_announcements, name="delete_announcement"),
    path("", views.get_announcements, name="announcement"),
]
