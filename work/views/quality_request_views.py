from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import QualityInspectionRequest

from ..services.quality_request_services import (
    assign_user_for_qty_request,
    create_quality_request_service,
    delete_qty_requests_service,
    get_qty_request_list_by_user,
    read_qty_request_service,
    update_quality_request_service,
)


# 품질검사 의뢰서 목록
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


# 품질검사 의뢰서 작성
@login_required(login_url="/user/login/")
def create_quality_request(request):
    return create_quality_request_service(request)


# 품질검사 의뢰서 수정
@login_required(login_url="/user/login/")
def update_quality_request(request, pk):
    return update_quality_request_service(request, pk)


# 품질검사 의뢰서 조회
@login_required(login_url="/user/login/")
def read_quality_request(request, pk):
    qty_request = read_qty_request_service(pk)
    return render(
        request,
        "work/quality/quality_request/read_quality_request.html",
        {"qty_request": qty_request},
    )


# 품질검사 의뢰서 서명 요청
@login_required(login_url="/user/login/")
def require_sign_quality_request(request):
    if request.method == "POST":
        doc = QualityInspectionRequest.objects.get(docNum=request.POST.get("docNum"))
        base_link = (
            "/work/update_quality_request/"
            if request.user.class2 != "일반 건설사업관리기술인"
            else "/work/read_quality_request/"
        )
        link = request.build_absolute_uri(base_link + str(doc.docNum))
        assign_user_for_qty_request(
            request.user,
            doc,
            int(request.POST.get("sign", 1)),
            link,
        )
        return redirect("work:quality_request")
    return Http404("잘못된 접근입니다.")


# 품질검사 의뢰서 삭제
@login_required(login_url="/user/login/")
def delete_qty_requests(request):
    return delete_qty_requests_service(request)
