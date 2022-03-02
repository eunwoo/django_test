from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import QualityInspectionRequest
from work.services.common_services import assign_user

from ..services.quality_request_services import (
    create_quality_request_service,
    get_qty_request_list_by_user,
    qty_request_success,
    read_qty_request_service,
    update_quality_request_service,
)


@login_required(login_url="/user/login/")
def quality_request(request):
    page = request.GET.get("page", 1)

    qty_request_list = get_qty_request_list_by_user(request.user)

    paginator = Paginator(qty_request_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "work/quality/quality_request/quality_request.html",
        {"qty_request_items": page_obj},
    )


@login_required(login_url="/user/login/")
def create_quality_request(request):
    return create_quality_request_service(request)


@login_required(login_url="/user/login/")
def update_quality_request(request, pk):
    return update_quality_request_service(request, pk)


@login_required(login_url="/user/login/")
def read_quality_request(request, pk):
    qty_request = read_qty_request_service(request.user, pk)
    return render(
        request,
        "work/quality/quality_request/read_quality_request.html",
        {"qty_request": qty_request},
    )


@login_required(login_url="/user/login/")
def require_sign_quality_request(request):
    if request.method == "POST":
        if request.user.class2 == "일반 건설사업관리기술인":
            qty_request_success(request.POST.get("docNum"))
        else:
            doc = QualityInspectionRequest.objects.get(
                docNum=request.POST.get("docNum")
            )
            assign_user(doc, int(request.POST.get("sign")))
        return redirect("work:quality_request")
    return Http404("잘못된 접근입니다.")
