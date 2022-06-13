from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from system_manager.models import Field

from system_manager.models import InstallLocate

from ..models import QualityInspectionRequest
from ..forms.quality_request_forms import (
    AgentQualityInspectionRequestForm,
    GeneralManagerQualityInspectionRequestForm,
)
from user.models import CustomUser

from ..services.common_services import sms_send
from django.contrib import messages


# 품질검사 의뢰서 목록 조회
def get_qty_request_list_by_user(user):
    if user.class2 == "일반 사용자":
        return QualityInspectionRequest.objects.filter(
            writerId=user,
            isSuccess=False,
        ).order_by(
            "isCheckManager",
            "-docNum",
        )
    elif user.class2 == "현장 대리인":
        return QualityInspectionRequest.objects.filter(
            agentId=user,
            isSuccess=False,
        ).order_by(
            "isCheckAgent",
            "-docNum",
        )
    else:
        return QualityInspectionRequest.objects.filter(
            generalEngineerId=user,
            isSuccess=False,
        ).order_by("-docNum")


# 품질검사 의뢰서 생성
def create_quality_request_service(request):
    field = Field.objects.get(pk=1)  # 현장 관리는 하나만 있음
    if request.method == "POST":
        form = GeneralManagerQualityInspectionRequestForm(request.POST)
        if form.is_valid():
            qty_req = form.save(commit=False)
            qty_req.writerId = request.user
            qty_req.fieldId = field
            qty_req.save()
            locates = request.POST.getlist("locate[]")
            for locate_id in locates:
                locate = InstallLocate.objects.get(pk=int(locate_id))
                qty_req.locateId.add(locate)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = GeneralManagerQualityInspectionRequestForm()
    last_doc = QualityInspectionRequest.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1
    return render(
        request,
        "work/quality/quality_request/create_quality_request.html",
        {"form": form, "docNum": docNum, "field": field},
    )


# 품질검사 의뢰서 수정
def update_quality_request_service(request, docNum):
    if request.user.class2 == "일반 사용자":
        return update_quality_request_for_generalManager(request, docNum)
    elif request.user.class2 == "현장 대리인":
        return update_quality_request_for_agent(request, docNum)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_quality_request_for_generalEngineer(request, docNum)
    return Http404()


# 일반관리자 품질검사 의뢰서 수정
def update_quality_request_for_generalManager(request, docNum):
    qty_req = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralManagerQualityInspectionRequestForm(
            request.POST, instance=qty_req
        )
        if form.is_valid():
            qty_req = form.save(commit=False)
            qty_req.writerId = request.user
            qty_req.save()
            qty_req.locateId.clear()
            locates = request.POST.getlist("locate[]")
            for locate_id in locates:
                locate = InstallLocate.objects.get(pk=int(locate_id))
                qty_req.locateId.add(locate)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = GeneralManagerQualityInspectionRequestForm(instance=qty_req)
    field = qty_req.fieldId
    return render(
        request,
        "work/quality/quality_request/update_quality_request.html",
        {"form": form, "docNum": qty_req.docNum, "field": field},
    )


# 현장대리인 품질검사 의뢰서 수정
def update_quality_request_for_agent(request, docNum):
    qty_req = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        form = AgentQualityInspectionRequestForm(request.POST, instance=qty_req)
        if form.is_valid():
            form.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = AgentQualityInspectionRequestForm(instance=qty_req)
    return render(
        request,
        "work/quality/quality_request/update_quality_request_agent.html",
        {"form": form},
    )


# 일반건설사업관리기술인 품질검사 의뢰서 수정
def update_quality_request_for_generalEngineer(request, docNum):
    qty_request = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        qty_request.isSaveGeneralEngineer = True
        qty_request.save()
        messages.success(request, "저장이 완료되었습니다.")
        return redirect("work:update_quality_request", qty_request.docNum)
    return render(
        request,
        "work/quality/quality_request/update_quality_request_generalEngineer.html",
        {"qty_request": qty_request},
    )


# 품질검사 의뢰서 유저 할당
def assign_user_for_qty_request(user, doc, user_pk: int, link):
    target_user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "일반 사용자":
        doc.agentId = target_user
        doc.isCheckAgent = False
        doc.isCheckManager = True
        sms_send(link, [target_user.phone])
    elif user.class2 == "현장 대리인":
        doc.generalEngineerId = target_user
        doc.isCheckAgent = True
        doc.isSuccess = False
        sms_send(link, [target_user.phone])
    else:
        doc.isSuccess = True
        sms_send(
            link,
            [
                doc.writerId.phone,
                doc.agentId.phone,
            ],
            1,
        )
    doc.save()
    return True


# 품질검사 의뢰서 조회
def read_qty_request_service(pk):
    qty_request = QualityInspectionRequest.objects.get(docNum=pk)
    return qty_request


# 품질검사 의뢰서 삭제
def delete_qty_requests_service(request):
    if request.method == "POST":
        qty_request_list = request.POST.getlist("delete_list[]")
        for qty_request in qty_request_list:
            qty_request = QualityInspectionRequest.objects.get(docNum=qty_request)
            qty_request.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)
