from django.urls import path
from . import views

app_name = "law"

urlpatterns = [
    path("create/", views.create_views, name="create_law"),
    path("update/<int:pk>/", views.update_views, name="update_law"),
    path("read/<int:pk>/", views.read_views, name="read_law"),
    path("", views.get_laws, name="law"),
]
