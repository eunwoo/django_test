from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from system_manager.models import Field

from ..models import (
    QualityPerformanceReport,
    QualityPerformanceFile,
    QualityPerformance,
)
from ..forms.quality_report_forms import (
    GeneralManagerQualityPerformanceReportForm,
)
from django.contrib import messages


# 품질검사 성과 보고서 작성
def get_qty_report_list_by_user(user):
    if user.class2 == "일반 사용자":
        return QualityPerformanceReport.objects.filter(
            writerId=user,
            isSuccess=False,
        ).order_by("isCheckManager", "-docNum")
    elif user.class2 == "현장 대리인":
        return QualityPerformanceReport.objects.filter(
            agentId=user,
            isSuccess=False,
        ).order_by("isCheckAgent", "-docNum")
    elif user.class2 == "일반 건설사업관리기술인":
        return QualityPerformanceReport.objects.filter(
            generalEngineerId=user,
            isSuccess=False,
        ).order_by("isCheckGeneralEngineer", "-docNum")
    else:
        return QualityPerformanceReport.objects.filter(
            totalEngineerId=user,
            isSuccess=False,
        ).order_by("-docNum")


# 품질검사 성과 보고서 조회
def read_qty_report_service(pk):
    qty_report = QualityPerformanceReport.objects.get(docNum=pk)
    return qty_report


# 품질검사 성과 보고서 작성
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
            files = request.FILES.getlist("docs_files")
            for file in files:
                docs_file = QualityPerformanceFile.objects.create(
                    title=file.name, doc=file, quality_performance_report_id=qty_report
                )
                docs_file.save()
            messages.success(request, "저장이 완료되었습니다.")
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


# 품질검사 성과 보고서 수정
def update_quality_report_service(request, pk):
    if request.user.class2 == "일반 사용자":
        return update_quality_report_general(request, pk)
    elif request.user.class2 == "현장 대리인":
        return update_quality_report_agent(request, pk)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_quality_report_generalEngineer(request, pk)
    elif request.user.class2 == "총괄 건설사업관리기술인":
        return update_quality_report_totalEngineer(request, pk)
    else:
        return Http404()


# 일반관리자 품질검사 성과 보고서 수정
def update_quality_report_general(request, pk):
    instance = QualityPerformanceReport.objects.get(docNum=pk)
    if request.method == "POST":
        form = GeneralManagerQualityPerformanceReportForm(
            request.POST, instance=instance
        )
        if form.is_valid():
            qty_report = form.save(commit=False)
            qty_report.writerId = request.user
            qty_report.save()
            qty_report.quality_performance.all().delete()
            create_quality_performance(request, qty_report)
            files = request.FILES.getlist("docs_files")
            if files:
                qty_report.quality_performance_file.all().delete()
            for file in files:
                docs_file = QualityPerformanceFile.objects.create(
                    title=file.name, doc=file, quality_performance_report_id=qty_report
                )
                docs_file.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_quality_report", qty_report.docNum)
    else:
        form = GeneralManagerQualityPerformanceReportForm(instance=instance)
    return render(
        request,
        "work/quality/quality_report/create_quality_report.html",
        {
            "form": form,
            "docNum": instance.docNum,
            "field": instance.fieldId,
            "doc": instance,
        },
    )


# 현장대리인 품질검사 성과 보고서 수정
def update_quality_report_agent(request, pk):
    qty_report = QualityPerformanceReport.objects.get(docNum=pk)
    if request.method == "POST":
        qty_report.isSaveAgent = True
        qty_report.save()
        messages.success(request, "저장이 완료되었습니다.")
        return redirect("work:update_quality_report", qty_report.docNum)
    return render(
        request,
        "work/quality/quality_report/update_quality_report_agent.html",
        {"qty_report": qty_report},
    )


# 일반 건설사업관리기술인 품질검사 성과 보고서 수정
def update_quality_report_generalEngineer(request, pk):
    qty_report = QualityPerformanceReport.objects.get(docNum=pk)
    if request.method == "POST":
        qty_report.isSaveGeneralEngineer = True
        qty_report.save()
        messages.success(request, "저장이 완료되었습니다.")
        return redirect("work:update_quality_report", qty_report.docNum)
    return render(
        request,
        "work/quality/quality_report/update_quality_report_generalEngineer.html",
        {"qty_report": qty_report},
    )


# 총괄 건설사업관리기술인 품질검사 성과 보고서 수정
def update_quality_report_totalEngineer(request, pk):
    qty_report = QualityPerformanceReport.objects.get(docNum=pk)
    if request.method == "POST":
        qty_report.isSaveTotalEngineer = True
        qty_report.save()
        messages.success(request, "저장이 완료되었습니다.")
        return redirect("work:update_quality_report", qty_report.docNum)
    return render(
        request,
        "work/quality/quality_report/update_quality_report_totalEngineer.html",
        {"qty_report": qty_report},
    )


# 품질검사 성과보고서 성과 목록 추가
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
            else False,  # 휨 하중 체크여부
            testType_zip=True
            if request.POST.getlist(form_list[3])[index] == "on"
            else False,  # 압축 하중 체크여부
            testType_tensile=True
            if request.POST.getlist(form_list[4])[index] == "on"
            else False,  # 인장 하중 체크여부
            plan=request.POST.getlist(form_list[5])[index],
            conducted=request.POST.getlist(form_list[6])[index],
            acceptance=request.POST.getlist(form_list[7])[index],
            failed=request.POST.getlist(form_list[8])[index],
            retest=request.POST.getlist(form_list[9])[index],
            add=request.POST.getlist(form_list[10])[index],
            quality_performance_report_id=qty_report,
        )
        performance.save()


# 품질검사 성과보고서 삭제
def delete_qty_reports_service(request):
    if request.method == "POST":
        qty_report_list = request.POST.getlist("delete_list[]")
        for qty_report in qty_report_list:
            qty_report = QualityPerformance.objects.get(docNum=qty_report)
            qty_report.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)
