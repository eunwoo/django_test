from django.urls import path

from . import views

app_name = "system_manager"


urlpatterns = [
    path("apply_field/", views.apply_field, name="apply_field"),  # 현장등록
    path("apply_locate/", views.apply_locate, name="apply_locate"),  # 설치위치명 등록
    path("apply_document/", views.apply_document, name="apply_document"),  # 문서 등록
    path(
        "user_management/", views.user_management, name="user_management"
    ),  # 사용자 등록 및 삭제
    path("delete_user/<int:pk>/", views.delete_user, name="delete_user"),  # 사용자 삭제
    path(
        "register_user/<int:pk>/", views.register_user, name="register_user"
    ),  # 사용자 등록
    path(
        "apply_document_template/<str:type>/",
        views.apply_document_template,
        name="apply_document_template",
    ),  # 문서 템플릿 등록
    path(
        "upload_documents/<str:type>/", views.upload_documents, name="upload_documents"
    ),  # 문서 업로드
    path(
        "delete_documents/<int:pk>/<str:type>",
        views.delete_documents,
        name="delete_documents",
    ),  # 문서 삭제
    path("", views.index, name="index"),
]
