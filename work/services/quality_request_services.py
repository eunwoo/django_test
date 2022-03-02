from django.shortcuts import render, redirect

from system_manager.models import Field

from system_manager.models import InstallLocate

from ..models import QualityInspectionRequest
from ..forms.quality_request_forms import GeneralManagerQualityInspectionRequestForm
from user.models import CustomUser


def get_qty_request_list_by_user(user):
    if user.class2 == "일반 관리자":
        return QualityInspectionRequest.objects.filter(writerId=user).order_by(
            "-isCheckManager", "-docNum"
        )
    elif user.class2 == "현장 대리인":
        return QualityInspectionRequest.objects.filter(agentId=user).order_by(
            "-isReadAgent", "-isCheckAgent", "-docNum"
        )
    else:
        return QualityInspectionRequest.objects.filter(generalEngineerId=user).order_by(
            "-isReadGeneralEngineer", "-isCheckGeneralEngineer", "-docNum"
        )


def assign_user_for_qty_request(doc, user_pk: int):
    user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "현장 대리인":
        doc.agentId = user
        doc.isReadAgent = False
    else:
        doc.totalEngineerId = user
        doc.isReadGeneralEngineer = True
        doc.isReadTotalEngineer = False
    doc.save()
    return True


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


def qty_request_success(docNum: int):
    qty_request = QualityInspectionRequest.objects.get(docNum=docNum)
    qty_request.isSuccess = True
    qty_request.isCheckManager = False
    qty_request.isCheckAgent = False
    qty_request.save()
    return True
