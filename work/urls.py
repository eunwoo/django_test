from django.urls import path

from .views import (
    main_views,
    safety_views,
    material_views,
    quality_request_views,
    quality_report_views,
)

app_name = "work"

main_url = [
    path("", main_views.index, name="index"),
    path("quality/", main_views.quality_menu, name="quality_menu"),
]

safety_url = [
    path("safety/", safety_views.safety, name="safety"),
    path("create_safety/", safety_views.create_safety, name="create_safety"),
    path("update_safety/<int:pk>/", safety_views.update_safety, name="update_safety"),
    path("get_users/", safety_views.get_users, name="get_users"),
    path("require_sign", safety_views.require_sign, name="require_sign"),
    path("read_safety/<int:pk>/", safety_views.read_safety, name="read_safety"),
    path(
        "create_checklist/<int:pk>/",
        safety_views.create_checklist,
        name="create_checklist",
    ),
    path(
        "read_checklist/<int:pk>/", safety_views.read_checklist, name="read_checklist"
    ),
]

material_url = [
    path("material/", material_views.material, name="material"),
    path("create_material/", material_views.create_material, name="create_material"),
]

quality_request_url = [
    path(
        "quality_request/",
        quality_request_views.quality_request,
        name="quality_request",
    ),
    path(
        "create_quality_request/",
        quality_request_views.create_quality_request,
        name="create_quality_request",
    ),
]

quality_report_url = [
    path("quality_report/", quality_report_views.quality_report, name="quality_report"),
    path(
        "create_quality_report/",
        quality_report_views.create_quality_report,
        name="create_quality_report",
    ),
]

urlpatterns = [
    *safety_url,
    *material_url,
    *quality_request_url,
    *quality_report_url,
    *main_url,
]
