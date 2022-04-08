from django.urls import path

from .views import (
    before_install_views,
    main_views,
    safety_views,
    material_views,
    quality_request_views,
    quality_report_views,
    install_views,
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
    path(
        "delete_safeties/",
        safety_views.delete_safeties,
        name="delete_safeties",
    ),
]

material_url = [
    path("material/", material_views.material, name="material"),
    path(
        "create_material/",
        material_views.create_material,
        name="create_material",
    ),
    path(
        "update_material/<int:pk>/",
        material_views.update_material,
        name="update_material",
    ),
    path(
        "require_sign_material/",
        material_views.require_sign_material,
        name="require_sign_material",
    ),
    path(
        "read_material/<int:pk>/",
        material_views.read_material,
        name="read_material",
    ),
    path(
        "delete_materials/",
        material_views.delete_materials,
        name="delete_materials",
    ),
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
    path(
        "update_quality_request/<int:pk>/",
        quality_request_views.update_quality_request,
        name="update_quality_request",
    ),
    path(
        "require_sign_quality_request/",
        quality_request_views.require_sign_quality_request,
        name="require_sign_quality_request",
    ),
    path(
        "read_quality_request/<int:pk>/",
        quality_request_views.read_quality_request,
        name="read_quality_request",
    ),
]

quality_report_url = [
    path(
        "quality_report/",
        quality_report_views.quality_report,
        name="quality_report",
    ),
    path(
        "create_quality_report/",
        quality_report_views.create_quality_report,
        name="create_quality_report",
    ),
    path(
        "update_quality_report/<int:pk>/",
        quality_report_views.update_quality_report,
        name="update_quality_report",
    ),
    path(
        "require_sign_quality_report/",
        quality_report_views.require_sign_quality_report,
        name="require_sign_quality_report",
    ),
    path(
        "read_quality_report/<int:pk>/",
        quality_report_views.read_quality_report,
        name="read_quality_report",
    ),
]

before_install_check_url = [
    path(
        "install_check/",
        before_install_views.select_type,
        name="install_check",
    ),
    path(
        "install_check/<str:type>/",
        before_install_views.select_install,
        name="select_install",
    ),
    path(
        "before_install/<str:type>/",
        before_install_views.before_install,
        name="before_install",
    ),
    path(
        "before_install_checklist/<str:type>/",
        before_install_views.before_install_checklist,
        name="before_install_checklist",
    ),
    path(
        "update_before_install_checklist/<str:type>/<int:pk>/",
        before_install_views.update_before_install_checklist,
        name="update_before_install_checklist",
    ),
    path(
        "cm_list",
        before_install_views.get_users,
        name="get_cms",
    ),
    path(
        "required_cm/<str:type>/",
        before_install_views.required_cm,
        name="required_cm",
    ),
    path(
        "read_before_install/<str:type>/<int:pk>/",
        before_install_views.read_before_checklist,
        name="read_before_checklist",
    ),
]

install_check_url = [
    path(
        "install/<str:type>/",
        install_views.install,
        name="install",
    ),
    path(
        "install_checklist/<str:type>/",
        install_views.install_checklist,
        name="install_checklist",
    ),
    path(
        "update_install_checklist/<str:type>/<int:pk>/",
        install_views.update_install_checklist,
        name="update_install_checklist",
    ),
    path(
        "read_install/<str:type>/<int:pk>/",
        install_views.read_checklist,
        name="read_checklist",
    ),
    path(
        "required_cm_install/<str:type>/",
        install_views.required_cm,
        name="required_cm_install",
    ),
]

urlpatterns = [
    *safety_url,
    *material_url,
    *quality_request_url,
    *quality_report_url,
    *before_install_check_url,
    *install_check_url,
    *main_url,
]
