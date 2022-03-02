from django.urls import path

from .views import (
    document_views,
    field_views,
    locate_views,
    main_views,
    user_management_views,
)

app_name = "system_manager"

locate_api = [
    path("locate/<int:class_type>/", locate_views.read_locate_class, name="get_locate"),
]

urlpatterns = [
    *locate_api,
    # 현장 관리
    path("manage_field/", field_views.manage_field, name="manage_field"),
    # 현장 등록 및 수정
    path("apply_field/", field_views.apply_field, name="apply_field"),
    # 조립 가설기자재 관리
    path("manage_equipments", field_views.manage_equipments, name="manage_equipments"),
    # 조립 가설기자재 등록
    path("apply_equipments/", field_views.apply_equipments, name="apply_equipments"),
    # 전문건설업체 관리자 연락처
    path("manage_cm_calls/", field_views.manage_cm_calls, name="manage_cm_calls"),
    # 전문건설업체 관리자 연락처 삭제
    path(
        "delete_cm_calls/<int:pk>", field_views.delete_cm_calls, name="delete_cm_calls"
    ),
    # 설치위치명 등록
    path("apply_locate/", locate_views.apply_locate, name="apply_locate"),
    # 사용자 등록 및 삭제
    path(
        "user_management/",
        user_management_views.user_management,
        name="user_management",
    ),
    # 사용자 삭제
    path(
        "delete_user/<int:pk>/", user_management_views.delete_user, name="delete_user"
    ),
    # 사용자 등록
    path(
        "register_user/<int:pk>/",
        user_management_views.register_user,
        name="register_user",
    ),
    # 문서 템플릿 등록
    path(
        "apply_document_template/<str:type>/",
        document_views.apply_document_template,
        name="apply_document_template",
    ),
    # 문서 등록
    path("apply_document/", document_views.apply_document, name="apply_document"),
    # 문서 업로드
    path(
        "upload_documents/<str:type>/",
        document_views.upload_documents,
        name="upload_documents",
    ),
    # 문서 삭제
    path(
        "delete_documents/<int:pk>/<str:type>",
        document_views.delete_documents,
        name="delete_documents",
    ),
    # 구조 안전성, 시공상세도면 메뉴
    path("detail_menu/<str:type>/", document_views.detail_menu, name="detail_menu"),
    # 메인 메뉴
    path("", main_views.index, name="index"),
]
