from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from work.services.common_services import assign_user
from ..models import SafetyCheckMenu, SafetyReport
from ..services.safety_services import (
    create_checklist_service,
    create_safety_service,
    delete_safeties,
    get_sign_users,
    read_checklist_service,
    read_safety_service,
    update_safety_agent,
    update_safety_general,
    get_safety_list_by_user,
    update_safety_generalEngineer,
    update_safety_totalEngineer,
)


@login_required(login_url="/user/login/")
def safety(request):
    page = request.GET.get("page", 1)

    safety_list = get_safety_list_by_user(request.user)

    paginator = Paginator(safety_list, 10)
    page_obj = paginator.get_page(page)

    return render(request, "work/safety/safety.html", {"safetyitems": page_obj})


@login_required(login_url="/user/login/")
def create_safety(request):
    return create_safety_service(request)


@login_required(login_url="/user/login/")
def read_safety(request, pk):
    safety = read_safety_service(request.user, pk)
    safety_url = list(map(lambda x: x.file.url, safety.docs.all()))
    return render(
        request,
        "work/safety/read_safety.html",
        {
            "safety": safety,
            "safety_url": safety_url,
        },
    )


@login_required(login_url="/user/login/")
def update_safety(request, pk):
    if request.user.class2 == "일반 관리자":
        return update_safety_general(request, pk)
    elif request.user.class2 == "현장 대리인":
        return update_safety_agent(request, pk)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_safety_generalEngineer(request, pk)
    elif request.user.class2 == "총괄 건설사업관리기술인":
        return update_safety_totalEngineer(request, pk)
    # 각 관리자 별로 IF 문 생성
    return Http404("잘못된 접근입니다.")


@login_required(login_url="/user/login/")
def get_users(request):
    users = get_sign_users(request)
    return JsonResponse(
        {"users": list(users.values("id", "name"))},
        json_dumps_params={"ensure_ascii": False},
    )


# 메일 전송 및 문자 전송
@login_required(login_url="/user/login/")
def require_sign(request):
    if request.method == "POST":
        doc = SafetyReport.objects.get(docNum=int(request.POST.get("docNum")))
        base_link = (
            "/work/update_safety/"
            if request.user.class2 != "총괄 건설사업관리기술인"
            else "/work/read_safety/"
        )
        link = request.build_absolute_uri(base_link + str(doc.docNum))
        assign_user(
            request.user,
            doc,
            int(request.POST.get("sign", 1)),
            link,
        )
        return redirect("work:safety")
    return Http404("잘못된 접근입니다.")


@login_required(login_url="/user/login/")
def create_checklist(request, pk):
    if request.user.class2 != "일반 건설사업관리기술인":
        return Http404("잘못된 접근입니다.")
    if request.method == "POST":
        create_checklist_service(request, pk)
        return redirect("work:safety")
    # 구조 일반 사항
    checklist1 = SafetyCheckMenu.objects.filter(checkType_id=1).order_by("pk")
    # 설계하중
    checklist2 = SafetyCheckMenu.objects.filter(checkType_id=2).order_by("pk")
    # 구조해석
    checklist3 = SafetyCheckMenu.objects.filter(checkType_id=3).order_by("pk")
    # 구조검토
    checklist4 = SafetyCheckMenu.objects.filter(checkType_id=4).order_by("pk")
    return render(
        request,
        "work/safety/checklist.html",
        {"checklist": [checklist1, checklist2, checklist3, checklist4], "docNum": pk},
    )


@login_required(login_url="/user/login/")
def read_checklist(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    checklist = read_checklist_service(safety)
    return render(
        request,
        "work/safety/read_checklist.html",
        {"safety": safety, "checklist": checklist},
    )


@login_required(login_url="/user/login/")
def delete_safety(request):
    return delete_safeties(request)
