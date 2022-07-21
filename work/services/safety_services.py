from django.http import JsonResponse
from django.shortcuts import render, redirect

from system_manager.models import DocsFile, EquipmentTypes, InstallLocate
from user.models import CustomUser

from ..forms.safety_forms import (
    GeneralEngineerSafetyReportForm,
    GeneralManagerSafetyReportForm,
    TotalEngineerSafetyReportForm,
)
from ..models import (
    SafetyCheckType,
    SafetyReport,
    SafetyCheckMenu,
    SafetyCheckList,
)
from django.contrib import messages


# 구조 안전성 검토 문서 목록 로드
def get_safety_list_by_user(user):
    if user.class2 == "일반 사용자":
        return SafetyReport.objects.filter(
            writerId=user,
            isSuccess=False,
        ).order_by("isCheckManager", "-docNum")
    elif user.class2 == "현장 대리인":
        return SafetyReport.objects.filter(
            agentId=user,
            isSuccess=False,
        ).order_by("isCheckAgent", "-docNum")
    elif user.class2 == "일반 건설사업관리기술인":
        return SafetyReport.objects.filter(
            generalEngineerId=user,
            isSuccess=False,
        ).order_by("isCheckGeneralEngineer", "-docNum")
    else:
        return SafetyReport.objects.filter(
            totalEngineerId=user,
            isSuccess=False,
        ).order_by("-docNum")


# 요청자에 따른 유저 목록 로드
def get_sign_users(request):
    if request.user.class2 == "일반 사용자":
        users = CustomUser.objects.filter(class2="현장 대리인", register=True)
    elif request.user.class2 == "현장 대리인":
        users = CustomUser.objects.filter(class2="일반 건설사업관리기술인", register=True)
    else:
        users = CustomUser.objects.filter(class2="총괄 건설사업관리기술인", register=True)
    return users


# 구조 안전성 검토 문서 로드
def read_safety_service(pk):
    safety = SafetyReport.objects.get(docNum=pk)
    return safety


# 일반관리자 구조 안전성 검토 문서 생성
def create_safety_service(request):
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.writerId = request.user
            locates = request.POST.getlist("locate[]")
            files = request.POST.getlist("docs[]")
            safety.save()
            safety.locateId.clear()
            for locate_id in locates:  # 설치위치 등록
                locate = InstallLocate.objects.get(pk=int(locate_id))
                safety.locateId.add(locate)
            safety.docs.clear()
            for file_id in files:  # 첨부파일 등록
                doc_file = DocsFile.objects.get(pk=int(file_id))
                safety.docs.add(doc_file)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralManagerSafetyReportForm()
        safety = form.save(commit=False)
        safety.writerId = request.user
        locates = request.POST.getlist("locate[]")
        files = request.POST.getlist("docs[]")
        safety.save()
        return redirect("work:update_safety", safety.docNum)

    # # 문서 번호 로드
    # last_doc = SafetyReport.objects.last()
    # if not last_doc:  # 처음 작성할 문서의 경우
    #     docNum = 1
    # else:
    #     docNum = last_doc.docNum + 1

    # # 관련 문서 로드
    # construct_bills1 = DocsFile.objects.filter(type="구조 계산서-강관 비계")
    # construct_bills2 = DocsFile.objects.filter(type="구조 계산서-시스템 비계")
    # construct_bills3 = DocsFile.objects.filter(type="구조 계산서-시스템 동바리")
    # detail_drawings1 = DocsFile.objects.filter(type="시공상세도면-강관 비계")
    # detail_drawings2 = DocsFile.objects.filter(type="시공상세도면-시스템 비계")
    # detail_drawings3 = DocsFile.objects.filter(type="시공상세도면-시스템 동바리")

    # equipment_list = list(EquipmentTypes.objects.all().values_list("isActive"))
    # equipment_list = list(map(lambda x: x[0], equipment_list))

    # return render(
    #     request,
    #     "work/safety/create_safety_general.html",
    #     {
    #         "docNum": docNum,
    #         "form": form,
    #         "construct_bills": [
    #             construct_bills1,
    #             construct_bills2,
    #             construct_bills3,
    #         ],
    #         "detail_drawings": [
    #             detail_drawings1,
    #             detail_drawings2,
    #             detail_drawings3,
    #         ],
    #         "equipment_list": equipment_list,
    #     },
    # )


# 일반관리자 구조 안전성 검토 문서 수정
def update_safety_general(request, pk):
    instance = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST, instance=instance)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.writerId = request.user
            files = request.POST.getlist("docs[]")
            locates = request.POST.getlist("locate[]")
            safety.save()
            if locates:
                safety.locateId.clear()
                for locate_id in locates:
                    locate = InstallLocate.objects.get(pk=int(locate_id))
                    safety.locateId.add(locate)
            if files:
                safety.docs.clear()
                for file_id in files:
                    doc_file = DocsFile.objects.get(pk=int(file_id))
                    safety.docs.add(doc_file)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralManagerSafetyReportForm(instance=instance)

    target_doc = SafetyReport.objects.get(docNum=pk)

    # 관련 문서 로드
    construct_bills1 = DocsFile.objects.filter(type="구조 계산서-강관 비계")
    construct_bills2 = DocsFile.objects.filter(type="구조 계산서-시스템 비계")
    construct_bills3 = DocsFile.objects.filter(type="구조 계산서-시스템 동바리")
    detail_drawings1 = DocsFile.objects.filter(type="시공상셰도면-강관 비계")
    detail_drawings2 = DocsFile.objects.filter(type="시공상셰도면-시스템 비계")
    detail_drawings3 = DocsFile.objects.filter(type="시공상셰도면-시스템 동바리")

    construct_bills_list = target_doc.docs.filter(type__contains="구조 계산서")
    detail_drawings_list = target_doc.docs.filter(type__contains="시공상세도면")

    equipment_list = list(EquipmentTypes.objects.all().values_list("isActive"))
    equipment_list = list(map(lambda x: x[0], equipment_list))

    return render(
        request,
        "work/safety/create_safety_general.html",
        {
            "docNum": pk,
            "form": form,
            "safety_locate": instance.locateId.all(),
            "construct_bills": [
                construct_bills1,
                construct_bills2,
                construct_bills3,
            ],
            "detail_drawings": [
                detail_drawings1,
                detail_drawings2,
                detail_drawings3,
            ],
            "construct_bills_list": construct_bills_list,
            "detail_drawings_list": detail_drawings_list,
            "equipment_list": equipment_list,
        },
    )


# 구조 안전성 신고서 현장대리인
def update_safety_agent(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        safety.isSaveAgent = True
        safety.save()
        messages.success(request, "저장이 완료되었습니다.")
        return redirect("work:update_safety", safety.docNum)
    print("update_safety_agent")
    print(request.user.password)
    return render(
        request,
        "work/safety/create_safety_agent.html",
        {"safety": safety},
    )


# 구조 안전성 신고서 일반건설사업기술인
def update_safety_generalEngineer(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = GeneralEngineerSafetyReportForm(request.POST, instance=safety)
        if form.is_valid():
            safety.isSaveGeneralEngineer = True
            safety = form.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralEngineerSafetyReportForm(instance=safety)
    return render(
        request,
        "work/safety/create_safety_generalEngineer.html",
        {"safety": safety, "form": form},
    )


# 구조 안전성 신고서 총괄건설사업기술인
def update_safety_totalEngineer(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = TotalEngineerSafetyReportForm(request.POST, instance=safety)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.isSaveTotalEngineer = True
            safety.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_safety", safety.docNum)
    else:
        form = TotalEngineerSafetyReportForm(instance=safety)
    return render(
        request,
        "work/safety/create_safety_totalEngineer.html",
        {"safety": safety, "form": form},
    )


# 구조 안전성 신고서 체크리스트 조회
def read_checklist_service(safety):
    safety_checklist = safety.safety_check_list.all()
    checklist = [[], [], [], []]
    for checklist_menu in safety_checklist:
        checkTypeId = checklist_menu.safetyCheckMenuId.checkType_id
        checklist[checkTypeId - 1].append(checklist_menu)
    return checklist


# 구조 안전성 신고서 체크리스트 제작
def create_checklist_service(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    print("create_checklist_service.")
    # print(safety.safety_check_list.all())
    safety.checklistConstructType = request.POST.get("constructType")
    safety.checklistDate = request.POST.get("date")
    safety.checklistTitle = request.POST.get("title")
    checklist = list(request.POST.keys())
    delete_list = ["csrfmiddlewaretoken", "constructType", "date", "title"]
    for delete_item in delete_list:
        checklist.remove(delete_item)
    if len(safety.safety_check_list.all()) == 0:
        for item in checklist:
            result = request.POST.get(item)
            checkitem = SafetyCheckList(
                safetyReportId=safety,
                safetyCheckMenuId=SafetyCheckMenu.objects.get(pk=int(item)),
                result=result,
            )
            checkitem.save()
    else:
        print("update checklist")
        # print(checklist)
        for item in checklist:
            result = request.POST.get(item)
            print(result)
            checkitem = SafetyCheckList.objects.get(
                safetyReportId=safety,
                safetyCheckMenuId=SafetyCheckMenu.objects.get(pk=int(item)),
            )
            checkitem.result = result
            checkitem.save(update_fields=["result"])

    print('checklist date')
    print(safety.checklistDate)
    if safety.checklistDate == "":
        safety.checklistDate = None
    safety.save(update_fields=["checklistDate", "checklistConstructType", "checklistTitle"])


# 구조 안전성 신고서 삭제
def delete_safeties(request):
    if request.method == "POST":
        safety_list = request.POST.getlist("delete_list[]")
        for safety in safety_list:
            safety = SafetyReport.objects.get(docNum=safety)
            safety.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)


# 구조 안전성 신고서 체크리스트 항목 추가
def create_checklist_item_service(category, content):
    new_item = SafetyCheckMenu(
        content=content,
        checkType=SafetyCheckType.objects.get(title=category),
    )
    new_item.save()
    return new_item.pk
