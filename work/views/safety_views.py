from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from work.services.common_services import assign_user
from ..models import SafetyCheckMenu, SafetyReport, SafetyCheckList
from ..services.safety_services import (
    create_checklist_item_service,
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
import json


# 구조 안전성 검토 목록
@login_required(login_url="/user/login/")
def safety(request):
    page = request.GET.get("page", 1)

    safety_list = get_safety_list_by_user(request.user)

    paginator = Paginator(safety_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "work/safety/safety.html",
        {"safetyitems": page_obj},
    )


# 구조 안전성 검토 신고서 작성
@login_required(login_url="/user/login/")
def create_safety(request):
    return create_safety_service(request)


# 구조 안전성 검토 신고서 조회
@login_required(login_url="/user/login/")
def read_safety(request, pk):
    safety = read_safety_service(pk)
    safety_url = list(map(lambda x: x.file.url, safety.docs.all()))
    return render(
        request,
        "work/safety/read_safety.html",
        {
            "safety": safety,
            "safety_url": safety_url,
        },
    )


# 구조 안전성 검토 신고서 수정
@login_required(login_url="/user/login/")
def update_safety(request, pk):
    if request.user.class2 == "일반 사용자":
        return update_safety_general(request, pk)
    elif request.user.class2 == "현장 대리인":
        # print("auth test")
        # print(check_password("dlfqksguswkd2", request.user.password))
        return update_safety_agent(request, pk)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_safety_generalEngineer(request, pk)
    elif request.user.class2 == "총괄 건설사업관리기술인":
        return update_safety_totalEngineer(request, pk)
    # 각 관리자 별로 IF 문 생성
    return Http404("잘못된 접근입니다.")


# 유저 목록 로드
@login_required(login_url="/user/login/")
def get_users(request):
    users = get_sign_users(request)
    return JsonResponse(
        {"users": list(users.values("id", "name"))},
        json_dumps_params={"ensure_ascii": False},
    )


# 패스워드 체크
@login_required(login_url="/user/login/")
def is_password_true(request):
    print("check_password")
    if request.method == "POST":
        print("POST")
        print(request.body)
        data_bytes = request.body.decode("utf-8")
        print(data_bytes)
        data = json.loads(data_bytes)
        print(data)
        print(data["password"])
        print(request.user.password)
        result = check_password(data["password"], request.user.password)
        print(result)
        return JsonResponse(
            {"success": result},
            json_dumps_params={"ensure_ascii": False},
        )
    return Http404("잘못된 접근입니다.")


# 문자 전송
@login_required(login_url="/user/login/")
def require_sign(request):
    if request.method == "POST":
        doc = SafetyReport.objects.get(docNum=int(request.POST.get("docNum")))
        base_link = (
            "/work/update_safety/"
            if request.user.class2 != "총괄 건설사업관리기술인"
            else "/work/read_safety/"
        )
        if request.user.class2 == "현장 대리인":
            doc.requested_at = timezone.now()
        link = request.build_absolute_uri(base_link + str(doc.docNum))
        assign_user(
            request.user,
            doc,
            int(request.POST.get("sign", 1)),
            link,
        )
        return redirect("work:safety")
    return Http404("잘못된 접근입니다.")


# 구조 안전성 검토 체크리스트 작성
@login_required(login_url="/user/login/")
def create_checklist(request, pk):
    if request.user.class2 != "일반 건설사업관리기술인":
        return Http404("잘못된 접근입니다.")
    if request.method == "POST":
        print('create_checklist - POST')
        create_checklist_service(request, pk)
        return redirect("work:update_safety", pk)
    # 구조 일반 사항
    checklist1 = SafetyCheckMenu.objects.filter(
        checkType_id=1,
        initItem=True,
    ).order_by("pk")
    # 설계하중
    checklist2 = SafetyCheckMenu.objects.filter(
        checkType_id=2,
        initItem=True,
    ).order_by("pk")
    # 구조해석
    checklist3 = SafetyCheckMenu.objects.filter(
        checkType_id=3,
        initItem=True,
    ).order_by("pk")
    # 구조검토
    checklist4 = SafetyCheckMenu.objects.filter(
        checkType_id=4,
        initItem=True,
    ).order_by("pk")
    print("get previous checklist data...")
    print(checklist1)
    safety = SafetyReport.objects.get(docNum=pk)
    # checkitem = SafetyCheckList.objects.get(
    #     safetyReportId=safety,
    #     safetyCheckMenuId=SafetyCheckMenu.objects.get(pk=int(1)),
    # )
    checklist1val = SafetyCheckList.objects.filter(
        safetyReportId=safety,
        safetyCheckMenuId__in=checklist1,
    )
    checklist2val = SafetyCheckList.objects.filter(
        safetyReportId=safety,
        safetyCheckMenuId__in=checklist2,
    )
    checklist3val = SafetyCheckList.objects.filter(
        safetyReportId=safety,
        safetyCheckMenuId__in=checklist3,
    )
    checklist4val = SafetyCheckList.objects.filter(
        safetyReportId=safety,
        safetyCheckMenuId__in=checklist4,
    )
    print(len(checklist1val))
    if len(checklist1val) == 0:
        for item in checklist1:
                checkitem = SafetyCheckList(
                    safetyReportId=safety,
                    safetyCheckMenuId=item,
                )
                checkitem.save()        
        checklist1val = SafetyCheckList.objects.filter(
            safetyReportId=safety,
            safetyCheckMenuId__in=checklist1,
        )
    if len(checklist2val) == 0:
        for item in checklist2:
            checkitem = SafetyCheckList(
                safetyReportId=safety,
                safetyCheckMenuId=item,
            )
            checkitem.save()        
        checklist2val = SafetyCheckList.objects.filter(
            safetyReportId=safety,
            safetyCheckMenuId__in=checklist2,
        )
    if len(checklist3val) == 0:
        for item in checklist3:
            checkitem = SafetyCheckList(
                safetyReportId=safety,
                safetyCheckMenuId=item,
            )
            checkitem.save()        
        checklist3val = SafetyCheckList.objects.filter(
            safetyReportId=safety,
            safetyCheckMenuId__in=checklist3,
        )
    if len(checklist4val) == 0:
        for item in checklist4:
            checkitem = SafetyCheckList(
                safetyReportId=safety,
                safetyCheckMenuId=item,
            )
            checkitem.save()        
        checklist4val = SafetyCheckList.objects.filter(
            safetyReportId=safety,
            safetyCheckMenuId__in=checklist4,
        )            
    zipped = [
        [checklist1, zip(checklist1, checklist1val)],
        [checklist2, zip(checklist2, checklist2val)],
        [checklist3, zip(checklist3, checklist3val)],
        [checklist4, zip(checklist4, checklist4val)],
    ]
    return render(
        request,
        "work/safety/checklist.html",
        {
            "checklist": zipped,
            "docNum": pk,
            "report" : safety,
        },
    )


# 구조 안전성 검토 체크리스트 조회
@login_required(login_url="/user/login/")
def read_checklist(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    checklist = read_checklist_service(safety)
    return render(
        request,
        "work/safety/read_checklist.html",
        {"safety": safety, "checklist": checklist},
    )


# 구조 안전성 검토 체크리스트 삭제
@login_required(login_url="/user/login/")
def delete_safety(request):
    return delete_safeties(request)


# 구조 안전성 검토 체크리스트 항목 추가
@login_required(login_url="/user/login/")
def create_checklist_item(request):
    if request.method == "POST":
        content = request.POST.get("content")
        category = request.POST.get("category")
        pk = create_checklist_item_service(category, content)
        return JsonResponse({"pk": pk})
    return Http404()
