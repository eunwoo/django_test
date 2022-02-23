from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from system_manager.models import DocsFile
from ..models import SafetyReport
from ..forms.safety_forms import GeneralManagerSafetyReportForm


@login_required(login_url="/user/login/")
def safety(request):
    return render(request, "work/safety/safety.html")


@login_required(login_url="/user/login/")
def create_safety(request):
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.writerId = request.user
            files = request.POST.getlist("docs[]")
            safety.save()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                safety.docs.add(doc_file)
            return redirect("work:update_safety", safety.docNum)
    else:
        form = GeneralManagerSafetyReportForm()

    # 문서 번호 로드
    last_doc = SafetyReport.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1

    # 관련 문서 로드
    construct_bills1 = DocsFile.objects.filter(type="구조 계산서-강관 비계")
    construct_bills2 = DocsFile.objects.filter(type="구조 계산서-시스템 비계")
    construct_bills3 = DocsFile.objects.filter(type="구조 계산서-시스템 동바리")
    detail_drawings1 = DocsFile.objects.filter(type="시공상셰도면-강관 비계")
    detail_drawings2 = DocsFile.objects.filter(type="시공상셰도면-시스템 비계")
    detail_drawings3 = DocsFile.objects.filter(type="시공상셰도면-시스템 동바리")

    return render(
        request,
        "work/safety/create_safety_general.html",
        {
            "docNum": docNum,
            "form": form,
            "construct_bills": [construct_bills1, construct_bills2, construct_bills3],
            "detail_drawings": [detail_drawings1, detail_drawings2, detail_drawings3],
        },
    )


@login_required(login_url="/user/login/")
def update_safety(request, pk):
    if request.method == "POST":
        form = GeneralManagerSafetyReportForm(request.POST)
        if form.is_valid():
            safety = form.save(commit=False)
            safety.save()
            return redirect("work:update_safety", safety.docNum)
    doc = SafetyReport.objects.get(docNum=pk)
    form = GeneralManagerSafetyReportForm(instance=doc)
    return render(request, "work/safety/create_safety_general.html", {"form": form})


@login_required(login_url="/user/login/")
def require_sign(request, docNum):
    return render(request, "work/safety/update_safety.html", {"docNum": docNum})


@login_required(login_url="/user/login/")
def delete_safety(request, pk):
    pass


@login_required(login_url="/user/login/")
def read_checklist(request, pk):
    pass
