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


# 업무 초기페이지 및 품질 검사 선택 페이지
main_url = [
    path("", main_views.index, name="index"),  # 엄무 초기 페이지
    path("quality/", main_views.quality_menu, name="quality_menu"),  # 품질 검사 선택 페이지
]


# 구조 안전성 검토 페이지
safety_url = [
    path("safety/", safety_views.safety, name="safety"),  # 구조 안전성 검토 목록 페이지
    path(
        "create_safety/", safety_views.create_safety, name="create_safety"
    ),  # 구조 안전성 검토 신고서 작성
    path(
        "update_safety/<int:pk>/",
        safety_views.update_safety,
        name="update_safety",
    ),  # 구조 안전성 검토 신고서 수정
    path("get_users/", safety_views.get_users, name="get_users"),  # 서명 요청 사용자 조회
    path("require_sign", safety_views.require_sign, name="require_sign"),  # 서명 요청 전송
    path(
        "read_safety/<int:pk>/",
        safety_views.read_safety,
        name="read_safety",
    ),  # 구조 안전성 검토 신고서 조회
    path(
        "create_checklist/<int:pk>/",
        safety_views.create_checklist,
        name="create_checklist",
    ),  # 구조 안전성 검토 신고서 체크리스트 작성(일반 건설사업관리기술인 전용)
    path(
        "read_checklist/<int:pk>/",
        safety_views.read_checklist,
        name="read_checklist",
    ),  # 구조 안전성 검토 신고서 체크리스트 조회
    path(
        "delete_safeties/",
        safety_views.delete_safeties,
        name="delete_safeties",
    ),  # 구조 안전성 검토 신고서 삭제
    path(
        "create_checklist_item",
        safety_views.create_checklist_item,
        name="create_checklist_item",
    ),  # 구조 안전성 검토 신고서 체크리스트 아이템 추가
]


# 자재 공급원 신고 페이지
material_url = [
    path("material/", material_views.material, name="material"),  # 자재 공급원 문서 목록
    path(
        "create_material/",
        material_views.create_material,
        name="create_material",
    ),  # 자재 공급원 신고서 작성
    path(
        "update_material/<int:pk>/",
        material_views.update_material,
        name="update_material",
    ),  # 자재 공급원 신고서 수정
    path(
        "require_sign_material/",
        material_views.require_sign_material,
        name="require_sign_material",
    ),  # 자재 공급원 신고서 서명 요청
    path(
        "read_material/<int:pk>/",
        material_views.read_material,
        name="read_material",
    ),  # 자재 공급원 신고서 조회
    path(
        "delete_materials/",
        material_views.delete_materials,
        name="delete_materials",
    ),  # 자재 공급원 신고서 삭제
]


# 품질 검사 의뢰서 페이지
quality_request_url = [
    path(
        "quality_request/",
        quality_request_views.quality_request,
        name="quality_request",
    ),  # 품질 검사 의뢰서 목록
    path(
        "create_quality_request/",
        quality_request_views.create_quality_request,
        name="create_quality_request",
    ),  # 품질 검사 의뢰서 작성
    path(
        "update_quality_request/<int:pk>/",
        quality_request_views.update_quality_request,
        name="update_quality_request",
    ),  # 품질 검사 의뢰서 수정
    path(
        "require_sign_quality_request/",
        quality_request_views.require_sign_quality_request,
        name="require_sign_quality_request",
    ),  # 품질 검사 의뢰서 서명 요청
    path(
        "read_quality_request/<int:pk>/",
        quality_request_views.read_quality_request,
        name="read_quality_request",
    ),  # 품질 검사 의뢰서 조회
    path(
        "delete_quality_requests/",
        quality_request_views.delete_qty_requests,
        name="delete_quality_requests",
    ),  # 품질 검사 의뢰서 삭제
]


# 품질 검사 성과 보고서 페이지
quality_report_url = [
    path(
        "quality_report/",
        quality_report_views.quality_report,
        name="quality_report",
    ),  # 품질 검사 성과 보고서 목록
    path(
        "create_quality_report/",
        quality_report_views.create_quality_report,
        name="create_quality_report",
    ),  # 품질 검사 성과 보고서 작성
    path(
        "update_quality_report/<int:pk>/",
        quality_report_views.update_quality_report,
        name="update_quality_report",
    ),  # 품질 검사 성과 보고서 수정
    path(
        "require_sign_quality_report/",
        quality_report_views.require_sign_quality_report,
        name="require_sign_quality_report",
    ),  # 품질 검사 성과 보고서 서명 요청
    path(
        "read_quality_report/<int:pk>/",
        quality_report_views.read_quality_report,
        name="read_quality_report",
    ),  # 품질 검사 성과 보고서 조회
    path(
        "delete_quality_reports/",
        quality_report_views.delete_quality_report,
        name="delete_quality_reports",
    ),  # 품질 검사 성과 보고서 삭제
]


# 설치작업 전 체크리스트
before_install_check_url = [
    path(
        "install_check/",
        before_install_views.select_type,
        name="install_check",
    ),  # 설치작업 전 체크리스트 목록
    path(
        "install_check/<str:type>/",
        before_install_views.select_install,
        name="select_install",
    ),  # 설치작업 전 체크리스트 선택
    path(
        "before_install/<str:type>/",
        before_install_views.before_install,
        name="before_install",
    ),  # 설치작업 전 체크리스트 작성
    path(
        "before_install_checklist/<str:type>/",
        before_install_views.before_install_checklist,
        name="before_install_checklist",
    ),  # 설치작업 전 체크리스트 조회
    path(
        "update_before_install_checklist/<str:type>/<int:pk>/",
        before_install_views.update_before_install_checklist,
        name="update_before_install_checklist",
    ),  # 설치작업 전 체크리스트 수정
    path(
        "cm_list",
        before_install_views.get_users,
        name="get_cms",
    ),  # 설치작업 전 체크리스트 건설업체 관리자 목록 조회
    path(
        "required_cm/<str:type>/",
        before_install_views.required_cm,
        name="required_cm",
    ),  # 설치작업 전 체크리스트 건설업체 관리자 선택
    path(
        "read_before_install/<str:type>/<int:pk>/",
        before_install_views.read_before_checklist,
        name="read_before_checklist",
    ),  # 설치작업 전 체크리스트 조회
    path(
        "delete_before_install_checklists/",
        before_install_views.before_install_checklists_delete_service,
        name="delete_before_install_checklists",
    ),  # 설치작업 전 체크리스트 삭제
    path(
        "add_before_install_item/<str:type>/",
        before_install_views.add_before_install_item,
        name="add_before_install_item",
    ),  # 설치작업 전 체크리스트 아이템 추가
    path(
        "measure_before_install/<str:urlcode>/",
        before_install_views.measure_before_install,
        name="measure_before_install",
    ),  # 설치작업 전 체크리스트 CM 조치 페이지
    path(
        "review_before_install_checklist/<str:type>/<int:pk>/",
        before_install_views.review_before_install_checklist,
        name="review_before_install_checklist",
    ),  # 설치작업 전 체크리스트 검토 페이지
    path(
        "success_before_install_checklist/",
        before_install_views.success_before_checklist,
        name="success_before_checklist",
    ),  # 설치작업 전 체크리스트 마감
    path(
        "measure_success_before/<str:urlcode>/",
        before_install_views.measure_success_before,
        name="measure_success_before",
    ),  # 설치작업 전 체크리스트 CM 조치 완료
]


# 설치작업 중 체크리스트
install_check_url = [
    path(
        "install/<str:type>/",
        install_views.install,
        name="install",
    ),  # 설치작업 중 체크리스트 목록
    path(
        "install_checklist/<str:type>/",
        install_views.install_checklist,
        name="install_checklist",
    ),  # 설치작업 중 체크리스트 조회
    path(
        "update_install_checklist/<str:type>/<int:pk>/",
        install_views.update_install_checklist,
        name="update_install_checklist",
    ),  # 설치작업 중 체크리스트 수정
    path(
        "read_install/<str:type>/<int:pk>/",
        install_views.read_checklist,
        name="read_checklist",
    ),  # 설치작업 중 체크리스트 조회
    path(
        "required_cm_install/<str:type>/",
        install_views.required_cm,
        name="required_cm_install",
    ),  # 설치작업 중 체크리스트 건설업체 관리자 선택
    path(
        "delete_install_checklists/",
        install_views.delete_install_checklists,
        name="delete_install_checklists",
    ),  # 설치작업 중 체크리스트 삭제
    path(
        "add_install_item/<str:type>/",
        install_views.add_install_item,
        name="add_install_item",
    ),  # 설치작업 중 체크리스트 아이템 추가
    path(
        "measure_install/<str:urlcode>/",
        install_views.measure_install,
        name="measure_install",
    ),  # 설치작업 중 체크리스트 CM 조치 페이지
    path(
        "review_install_checklist/<str:type>/<int:pk>/",
        install_views.review_install_checklist,
        name="review_install_checklist",
    ),  # 설치작업 중 체크리스트 검토 페이지
    path(
        "success_install_checklist/",
        install_views.success_install_checklist,
        name="success_install_checklist",
    ),  # 설치작업 중 체크리스트 마감
    path(
        "measure_success/<str:urlcode>/",
        install_views.measure_success,
        name="measure_success",
    ),  # 설치작업 중 체크리스트 CM 조치 완료
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
