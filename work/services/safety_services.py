from django.shortcuts import render, redirect

from system_manager.models import DocsFile
from user.models import CustomUser

from ..forms.safety_forms import (
    GeneralEngineerSafetyReportForm,
    GeneralManagerSafetyReportForm,
    TotalEngineerSafetyReportForm,
)
from ..models import SafetyReport, SafetyCheckMenu, SafetyCheckList


def get_safety_list_by_user(user):
    if user.class2 == "일반 관리자":
        return SafetyReport.objects.filter(writerId=user).order_by(
            "-isCheckManager", "-docNum"
        )
    elif user.class2 == "현장 대리인":
        return SafetyReport.objects.filter(agentId=user).order_by(
            "-isReadAgent", "-isCheckAgent", "-docNum"
        )
    elif user.class2 == "일반 건설사업관리기술인":
        return SafetyReport.objects.filter(generalEngineerId=user).order_by(
            "-isReadGeneralEngineer", "-isCheckGeneralEngineer", "-docNum"
        )
    else:
        return SafetyReport.objects.filter(totalEngineerId=user).order_by(
            "-isReadTotalEngineer", "-isSuccess", "-docNum"
        )


def get_sign_users(request):
    if request.user.class2 == "일반 관리자":
        users = CustomUser.objects.filter(class2="현장 대리인", register=True)
    elif request.user.class2 == "현장 대리인":
        users = CustomUser.objects.filter(class2="일반 건설사업관리기술인", register=True)
    else:
        users = CustomUser.objects.filter(class2="총괄 건설사업관리기술인", register=True)
    return users


def assign_user(docNum: int, user_pk: int):
    safety = SafetyReport.objects.get(docNum=docNum)
    user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "현장 대리인":
        safety.agentId = user
        safety.isReadAgent = False
    elif user.class2 == "일반 건설사업관리기술인":
        safety.generalEngineerId = user
        safety.isReadAgent = True
        safety.isReadGeneralEngineer = False
    else:
        safety.totalEngineerId = user
        safety.isReadGeneralEngineer = True
        safety.isReadTotalEngineer = False
    safety.save()
    return True


def read_safety_service(user, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if user.class2 == "일반 관리자":
        safety.isCheckManager = True
    elif user.class2 == "현장 대리인":
        safety.isCheckAgent = True
    elif user.class2 == "일반 건설사업관리기술인":
        safety.isCheckGeneralEngineer = True
    safety.save()
    return safety


def safety_success(docNum: int):
    safety = SafetyReport.objects.get(docNum=docNum)
    # 메일전송 만들기
    safety.isSuccess = True
    safety.isCheckManager = False
    safety.isCheckAgent = False
    safety.isCheckGeneralEngineer = False
    safety.save()
    return True


def update_safety_general(request, pk):
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST, instance=pk)
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
        form = GeneralManagerSafetyReportForm(
            instance=SafetyReport.objects.get(docNum=pk)
        )

    target_doc = SafetyReport.objects.get(docNum=pk)
    docNum = target_doc.docNum

    # 관련 문서 로드
    construct_bills1 = DocsFile.objects.filter(type="구조 계산서-강관 비계")
    construct_bills2 = DocsFile.objects.filter(type="구조 계산서-시스템 비계")
    construct_bills3 = DocsFile.objects.filter(type="구조 계산서-시스템 동바리")
    detail_drawings1 = DocsFile.objects.filter(type="시공상셰도면-강관 비계")
    detail_drawings2 = DocsFile.objects.filter(type="시공상셰도면-시스템 비계")
    detail_drawings3 = DocsFile.objects.filter(type="시공상셰도면-시스템 동바리")

    construct_bills_list = target_doc.docs.filter(type__contains="구조 계산서")
    detail_drawings_list = target_doc.docs.filter(type__contains="시공상세도면")

    return render(
        request,
        "work/safety/create_safety_general.html",
        {
            "docNum": docNum,
            "form": form,
            "construct_bills": [construct_bills1, construct_bills2, construct_bills3],
            "detail_drawings": [detail_drawings1, detail_drawings2, detail_drawings3],
            "construct_bills_list": construct_bills_list,
            "detail_drawings_list": detail_drawings_list,
        },
    )


def update_safety_agent(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    return render(
        request,
        "work/safety/create_safety_agent.html",
        {"safety": safety},
    )


def update_safety_generalEngineer(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = GeneralEngineerSafetyReportForm(request.POST, instance=safety)
        if form.is_valid():
            safety = form.save()
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralEngineerSafetyReportForm(instance=safety)
    return render(
        request,
        "work/safety/create_safety_generalEngineer.html",
        {"safety": safety, "form": form},
    )


def update_safety_totalEngineer(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = TotalEngineerSafetyReportForm(request.POST, instance=safety)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.isSuccess = True
            safety.save()
            return redirect("work:update_safety", safety.docNum)
    else:
        form = TotalEngineerSafetyReportForm(instance=safety)
    return render(
        request,
        "work/safety/create_safety_totalEngineer.html",
        {"safety": safety, "form": form},
    )


def read_checklist_service(safety):
    safety_checklist = safety.safety_check_list.all()
    checklist = [[], [], [], []]
    for checklist_menu in safety_checklist:
        checkTypeId = checklist_menu.safetyCheckMenuId.checkType_id
        checklist[checkTypeId - 1].append(checklist_menu)
    return checklist


def create_checklist_service(request, pk):
    safety = SafetyReport.objects.get(docNum=pk)
    safety.checklistConstructType = request.POST.get("constructType")
    safety.checklistDate = request.POST.get("date")
    checklist = list(request.POST.keys())
    delete_list = ["csrfmiddlewaretoken", "constructType", "date"]
    for delete_item in delete_list:
        checklist.remove(delete_item)
    for item in checklist:
        result = request.POST.get(item)
        checkitem = SafetyCheckList(
            safetyReportId=safety,
            safetyCheckMenuId=SafetyCheckMenu.objects.get(pk=int(item)),
            result=result,
        )
        checkitem.save()
    safety.save()
