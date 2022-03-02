from django.http import Http404
from django.shortcuts import render, redirect

from system_manager.models import Field

from ..models import (
    QualityPerformanceReport,
    QualityPerformanceFile,
    QualityPerformance,
)
from ..forms.quality_report_forms import GeneralManagerQualityPerformanceReportForm


def create_quality_report_service(request):
    field = Field.objects.get(pk=1)  # 현장 관리는 하나만 있음
    last_doc = QualityPerformanceReport.objects.last()
    if request.method == "POST":
        form = GeneralManagerQualityPerformanceReportForm(request.POST)
        if form.is_valid():
            qty_report = form.save(commit=False)
            qty_report.writerId = request.user
            qty_report.fieldId = field
            qty_report.save()
            create_quality_performance(request, qty_report)
            files = request.FILES.getlist("doc_files")
            for file in files:
                docs_file = QualityPerformanceFile.objects.create(
                    title=file.name, doc=file, quality_performance_report_id=qty_report
                )
                docs_file.save()
            return redirect("work:update_quality_report", qty_report.docNum)
    else:
        form = GeneralManagerQualityPerformanceReportForm()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1
    return render(
        request,
        "work/quality/quality_report/create_quality_report.html",
        {"form": form, "docNum": docNum, "field": field},
    )


def update_quality_report_service(request, pk):
    instance = QualityPerformanceReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = GeneralManagerQualityPerformanceReportForm(
            request.POST, instance=instance
        )
        if form.is_valid():
            qty_report = form.save(commit=False)
            qty_report.writerId = request.user
            qty_report.quality_performance.clear()
            qty_report.quality_performance_file.clear()
            qty_report.save()
            create_quality_performance(request, qty_report)
            files = request.FILES.getlist("doc_files")
            for file in files:
                docs_file = QualityPerformanceFile.objects.create(
                    title=file.name, doc=file, quality_performance_report_id=qty_report
                )
                docs_file.save()
            return redirect("work:update_quality_report", qty_report.docNum)
    else:
        form = GeneralManagerQualityPerformanceReportForm(instance=instance)
    return render(
        request,
        "work/quality/quality_report/create_quality_report.html",
        {"form": form, "docNum": instance.docNum, "field": instance.fieldId},
    )


def create_quality_performance(request, qty_report):
    form_list = [
        "goods",
        "standard",
        "hweem",
        "zip",
        "tensile",
        "plan",
        "conducted",
        "acceptance",
        "failed",
        "retest",
        "add",
    ]
    form_length = len(request.POST.getlist("goods"))
    for index in range(form_length):
        performance = QualityPerformance.objects.create(
            goods=request.POST.getlist(form_list[0])[index],
            standard=request.POST.getlist(form_list[1])[index],
            testType_hweem=True
            if request.POST.getlist(form_list[2])[index] == "on"
            else False,
            testType_zip=True
            if request.POST.getlist(form_list[3])[index] == "on"
            else False,
            testType_tensile=True
            if request.POST.getlist(form_list[4])[index] == "on"
            else False,
            plan=request.POST.getlist(form_list[5])[index],
            conducted=request.POST.getlist(form_list[6])[index],
            acceptance=request.POST.getlist(form_list[7])[index],
            failed=request.POST.getlist(form_list[8])[index],
            retest=request.POST.getlist(form_list[9])[index],
            add=request.POST.getlist(form_list[10])[index],
            quality_performance_report_id=qty_report,
        )
        performance.save()
