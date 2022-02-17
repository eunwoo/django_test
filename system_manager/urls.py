from django.urls import path

from .views import (
    document_views,
    field_views,
    locate_views,
    main_views,
    user_management_views,
)

app_name = "system_manager"


urlpatterns = [
    # 현장등록
    path("apply_field/", field_views.apply_field, name="apply_field"),
    # 설치위치명 등록
    path("apply_locate/", locate_views.apply_locate, name="apply_locate"),
    # 문서 등록
    path("apply_document/", document_views.apply_document, name="apply_document"),
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
    # 메인 메뉴
    path("", main_views.index, name="index"),
]
