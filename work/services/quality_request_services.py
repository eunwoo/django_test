from django.http import Http404
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


def get_qty_request_list_by_user(user):
    if user.class2 == "일반 관리자":
        return QualityInspectionRequest.objects.filter(writerId=user).order_by(
            "isCheckManager", "-isSuccess", "-docNum"
        )
    elif user.class2 == "현장 대리인":
        return QualityInspectionRequest.objects.filter(agentId=user).order_by(
            "isCheckAgent", "-isSuccess", "-docNum"
        )
    else:
        return QualityInspectionRequest.objects.filter(generalEngineerId=user).order_by(
            "isSuccess", "-docNum"
        )


def create_quality_request_service(request):
    field = Field.objects.get(pk=1)  # 현장 관리는 하나만 있음
    if request.method == "POST":
        form = GeneralManagerQualityInspectionRequestForm(request.POST)
        if form.is_valid():
            qty_req = form.save(commit=False)
            qty_req.writerId = request.user
            qty_req.fieldId = field
            qty_req.locateId = InstallLocate.objects.get(pk=request.POST["locate"])
            qty_req.save()
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


def update_quality_request_service(request, docNum):
    if request.user.class2 == "일반 관리자":
        return update_quality_request_for_generalManager(request, docNum)
    elif request.user.class2 == "현장 대리인":
        return update_quality_request_for_agent(request, docNum)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_quality_request_for_generalEngineer(request, docNum)
    return Http404()


def update_quality_request_for_generalManager(request, docNum):
    qty_req = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralManagerQualityInspectionRequestForm(
            request.POST, instance=qty_req
        )
        if form.is_valid():
            qty_req = form.save(commit=False)
            qty_req.writerId = request.user
            if request.POST["locate"]:
                qty_req.locateId = InstallLocate.objects.get(pk=request.POST["locate"])
            qty_req.save()
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = GeneralManagerQualityInspectionRequestForm(instance=qty_req)
    field = qty_req.fieldId
    return render(
        request,
        "work/quality/quality_request/update_quality_request.html",
        {"form": form, "docNum": qty_req.docNum, "field": field},
    )


def update_quality_request_for_agent(request, docNum):
    qty_req = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        form = AgentQualityInspectionRequestForm(request.POST, instance=qty_req)
        if form.is_valid():
            form.save()
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = AgentQualityInspectionRequestForm(instance=qty_req)
    return render(
        request,
        "work/quality/quality_request/update_quality_request_agent.html",
        {"form": form},
    )


def update_quality_request_for_generalEngineer(request, docNum):
    qty_request = QualityInspectionRequest.objects.get(docNum=docNum)
    if request.method == "POST":
        qty_request.isSuccess = True
        qty_request.save()
        return redirect("work:update_quality_request", qty_request.docNum)
    return render(
        request,
        "work/quality/quality_request/update_quality_request_generalEngineer.html",
        {"qty_request": qty_request},
    )


def assign_user_for_qty_request(user, doc, user_pk: int, link):
    target_user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "일반 관리자":
        doc.agentId = target_user
        doc.isCheckAgent = False
        doc.isCheckManager = True
        sms_send(link, [target_user.phone])
    elif user.class2 == "현장 대리인":
        doc.generalEngineerId = target_user
        doc.isSuccess = False
        sms_send(link, [target_user.phone])
    else:
        doc.isSuccess = True
        doc.isCheckManager = False
        doc.isCheckAgent = False
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


def read_qty_request_service(user, pk):
    qty_request = QualityInspectionRequest.objects.get(docNum=pk)
    if user.class2 == "일반 관리자":
        qty_request.isCheckManager = True
    elif user.class2 == "현장 대리인":
        qty_request.isCheckAgent = True
    qty_request.save()
    return qty_request
