from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from system_manager.models import DocsFile
from user.models import CustomUser
from work.services.common_services import assign_user

from ..models import SafetyCheckMenu, SafetyReport
from ..forms.safety_forms import GeneralManagerSafetyReportForm
from ..services.safety_services import (
    create_checklist_service,
    get_sign_users,
    read_checklist_service,
    read_safety_service,
    safety_success,
    update_safety_agent,
    update_safety_general,
    get_safety_list_by_user,
    update_safety_generalEngineer,
    update_safety_totalEngineer,
)
from ..utils.send_alert import email_send


@login_required(login_url="/user/login/")
def safety(request):
    page = request.GET.get("page", 1)

    safety_list = get_safety_list_by_user(request.user)

    paginator = Paginator(safety_list, 10)
    page_obj = paginator.get_page(page)

    return render(request, "work/safety/safety.html", {"safetyitems": page_obj})


@login_required(login_url="/user/login/")
def create_safety(request):
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.writerId = request.user
            files = request.POST.getlist("docs[]")
            safety.save()
            safety.docs.clear()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                safety.docs.add(doc_file)
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralManagerSafetyReportForm()

    # 문서 번호 로드
    last_doc = SafetyReport.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1

    # 관련 문서 로드
    construct_bills1 = DocsFile.objects.filter(type="구조 계산서-강관 비계")
    construct_bills2 = DocsFile.objects.filter(type="구조 계산서-시스템 비계")
    construct_bills3 = DocsFile.objects.filter(type="구조 계산서-시스템 동바리")
    detail_drawings1 = DocsFile.objects.filter(type="시공상셰도면-강관 비계")
    detail_drawings2 = DocsFile.objects.filter(type="시공상셰도면-시스템 비계")
    detail_drawings3 = DocsFile.objects.filter(type="시공상셰도면-시스템 동바리")

    return render(
        request,
        "work/safety/create_safety_general.html",
        {
            "docNum": docNum,
            "form": form,
            "construct_bills": [construct_bills1, construct_bills2, construct_bills3],
            "detail_drawings": [detail_drawings1, detail_drawings2, detail_drawings3],
        },
    )


@login_required(login_url="/user/login/")
def read_safety(request, pk):
    safety = read_safety_service(request.user, pk)
    return render(
        request,
        "work/safety/read_safety.html",
        {"safety": safety},
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
        assign_user(request.user, doc, int(request.POST.get("sign", 1)))
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
def delete_safety(request, pk):
    pass
