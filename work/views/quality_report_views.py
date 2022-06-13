from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import QualityPerformanceReport
from work.services.common_services import assign_user

from ..services.quality_report_services import (
    create_quality_report_service,
    delete_qty_reports_service,
    get_qty_report_list_by_user,
    read_qty_report_service,
    update_quality_report_service,
)


# 품질검사 성과 보고서 목록
@login_required(login_url="/user/login/")
def quality_report(request):
    page = request.GET.get("page", 1)

    qty_request_list = get_qty_report_list_by_user(request.user)

    paginator = Paginator(qty_request_list, 10)
    page_obj = paginator.get_page(page)
    return render(
        request,
        "work/quality/quality_report/quality_report.html",
        {"qty_report_items": page_obj},
    )


# 품질검사 성과 보고서 조회
@login_required(login_url="/user/login/")
def read_quality_report(request, pk):
    qty_report = read_qty_report_service(pk)
    qty_report_file_url = list(
        map(lambda x: x.doc.url, qty_report.quality_performance_file.all())
    )
    return render(
        request,
        "work/quality/quality_report/read_quality_report.html",
        {
            "qty_report": qty_report,
            "qty_report_file_url": qty_report_file_url,
        },
    )


# 품질검사 성과 보고서 작성
@login_required(login_url="/user/login/")
def create_quality_report(request):
    return create_quality_report_service(request)


# 품질검사 성과 보고서 수정
@login_required(login_url="/user/login/")
def update_quality_report(request, pk):
    return update_quality_report_service(request, pk)


# 품질검사 성과 보고서 삭제
@login_required(login_url="/user/login/")
def delete_quality_report(request):
    return delete_qty_reports_service(request)


# 품질검사 성과 보고서 서명요청
@login_required(login_url="/user/login/")
def require_sign_quality_report(request):
    if request.method == "POST":
        doc = QualityPerformanceReport.objects.get(docNum=request.POST.get("docNum"))
        base_link = (
            "/work/update_quality_report/"
            if request.user.class2 != "총괄 건설사업관리기술인"
            else "/work/read_quality_report/"
        )
        link = request.build_absolute_uri(base_link + str(doc.docNum))
        assign_user(
            request.user,
            doc,
            int(request.POST.get("sign", 1)),
            link,
        )
        return redirect("work:quality_report")
    return Http404("잘못된 접근입니다.")
