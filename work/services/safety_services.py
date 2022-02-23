from django.shortcuts import render, redirect

from system_manager.models import DocsFile
from user.models import CustomUser

from ..forms.safety_forms import GeneralManagerSafetyReportForm
from ..models import SafetyReport


def get_sign_users(request):
    if request.user.class2 == "일반 관리자":
        users = CustomUser.objects.filter(class2="현장 대리인")
    else:
        users = CustomUser.objects.all()
    return users


def assign_user(docNum: int, user_pk: int):
    safety = SafetyReport.objects.get(docNum=docNum)
    safety.agentId = CustomUser.objects.get(pk=user_pk)
    safety.save()


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
