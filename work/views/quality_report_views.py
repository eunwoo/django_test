from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import QualityPerformanceReport
from work.services.common_services import assign_user

from ..services.quality_report_services import (
    create_quality_report_service,
    get_qty_report_list_by_user,
    qty_report_success,
    read_qty_report_service,
    update_quality_report_service,
)


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


@login_required(login_url="/user/login/")
def read_quality_report(request, pk):
    qty_report = read_qty_report_service(request.user, pk)
    return render(
        request,
        "work/quality/quality_report/read_quality_report.html",
        {"qty_report": qty_report},
    )


@login_required(login_url="/user/login/")
def create_quality_report(request):
    return create_quality_report_service(request)


@login_required(login_url="/user/login/")
def update_quality_report(request, pk):
    return update_quality_report_service(request, pk)


@login_required(login_url="/user/login/")
def delete_quality_report(request, pk):
    pass


@login_required(login_url="/user/login/")
def require_sign_quality_report(request):
    if request.method == "POST":
        doc = QualityPerformanceReport.objects.get(docNum=request.POST.get("docNum"))
        assign_user(request.user, doc, int(request.POST.get("sign", 1)))
        return redirect("work:quality_report")
    return Http404("잘못된 접근입니다.")
