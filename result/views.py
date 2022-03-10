from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.db.models import F

# Create your views here.


from work.models import (
    SafetyReport,
    MaterialSupplyReport,
    QualityInspectionRequest,
    QualityPerformanceReport,
    BeforeInstallCheckList,
    InstallCheckList,
)


@login_required(login_url="/user/login/")
def search(request):
    safety = (
        SafetyReport.objects.all()
        .values_list("docNum", "created_at")
        .annotate(type=Value("safety", output_field=CharField()))
    )
    material = (
        MaterialSupplyReport.objects.all()
        .values_list("docNum", "created_at")
        .annotate(type=Value("material", output_field=CharField()))
    )
    quality = (
        QualityInspectionRequest.objects.all()
        .values_list("docNum", "created_at")
        .annotate(type=Value("qty_request", output_field=CharField()))
    ).union(
        (
            QualityPerformanceReport.objects.all()
            .values_list("docNum", "created_at")
            .annotate(type=Value("qty_report", output_field=CharField()))
        )
    )
    checklist = (
        BeforeInstallCheckList.objects.all()
        .annotate(docNum=F("pk"))
        .values_list("docNum", "created_at")
        .annotate(type=Value("checklist", output_field=CharField()))
    )
    asdf = safety.union(checklist)
    return render(
        request,
        "result/search.html",
    )
