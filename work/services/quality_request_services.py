from django.shortcuts import render, redirect

from system_manager.models import Field

from ..models import QualityInspectionRequest
from ..forms.quality_request_forms import GeneralManagerQualityInspectionRequestForm


def create_quality_request_service(request):
    if request.method == "POST":
        form = GeneralManagerQualityInspectionRequestForm(request.POST)
        if form.is_valid():
            qty_req = form.save(commit=False)
            qty_req.writerId = request.user
            # qty_req.locateId = 수동으로 작성하기
            qty_req.save()
            return redirect("work:update_quality_request", qty_req.docNum)
    else:
        form = GeneralManagerQualityInspectionRequestForm()
    last_doc = QualityInspectionRequest.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1
    field = Field.objects.get(pk=1)  # 현장 관리는 하나만 있음
    return render(
        request,
        "work/quality/quality_request/create_quality_request.html",
        {"form": form, "docNum": docNum, "field": field},
    )
