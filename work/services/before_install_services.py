from django.shortcuts import render, redirect
from system_manager.models import InstallLocate
from work.forms.before_install_form import BeforeInstallCheckListForm
from django.contrib import messages

from work.models import (
    BeforeInspectionItem,
    BeforeInspectionResult,
    BeforeInstallCheckList,
)

from system_manager.models import ConstructManager

from ..services.common_services import sms_send


def assign_cm(request, type):
    cm = ConstructManager.objects.get(pk=request.POST.get("sign"))
    doc = BeforeInstallCheckList.objects.get(pk=request.POST.get("docNum"))
    doc.isSuccess = True
    doc.save()
    link = f"/read_before_install/{type}/{doc.pk}/"
    cm_phone = cm.phone
    sms_send(link, [cm_phone])
    # 문자 전송 페이지 만들기


def get_require_users():
    users = ConstructManager.objects.all()
    return users


def before_install_checklist_service(request, type: str):
    equipment = ""
    if type == "강관 비계":
        equipment = "1"
    elif type == "시스템 비계":
        equipment = "2"
    else:
        equipment = "3"
    if request.method == "POST":
        form = BeforeInstallCheckListForm(request.POST)
        if form.is_valid():
            before_checklist = form.save(commit=False)
            before_checklist.equipment = type
            before_checklist.writerId = request.user
            before_checklist.locateId = InstallLocate.objects.get(
                pk=request.POST["locate"]
            )
            pk_checklist = request.POST.getlist("checklist-pk")
            image_keys = request.FILES.keys()
            before_checklist.save()
            for pk in pk_checklist:
                result_item = BeforeInspectionResult(
                    result=request.POST[pk],
                    before_install_checklist_id=before_checklist,
                    before_inspection_item_id=BeforeInspectionItem.objects.get(pk=pk),
                )
                result_item.content = request.POST[f"{pk}-belong"]
                result_item.save()
                if f"{pk}-images[]" in image_keys:
                    images = request.FILES.getlist(f"{pk}-images[]")
                    for img in images:
                        result_item.measures.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect(
                "work:update_before_install_checklist", type, before_checklist.pk
            )
    else:
        form = BeforeInstallCheckListForm()
    checklist = BeforeInspectionItem.objects.filter(equipment=equipment)
    last_doc = BeforeInstallCheckList.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.pk + 1
    return render(
        request,
        "work/install/before/before_install_checklist.html",
        {
            "type": type,
            "checklist": checklist,
            "docNum": docNum,
            "form": form,
        },
    )


def update_before_checklist_service(request, type, pk):
    instance = BeforeInstallCheckList.objects.get(pk=pk)
    if request.method == "POST":
        form = BeforeInstallCheckListForm(request.POST, instance=instance)
        if form.is_valid():
            before_checklist = form.save(commit=False)
            before_checklist.equipment = type
            if "locate" in request.POST.keys():
                before_checklist.locateId = InstallLocate.objects.get(
                    pk=request.POST["locate"]
                )
            pk_checklist = request.POST.getlist("checklist-pk")
            image_keys = request.FILES.keys()
            before_checklist.before_inspection_result.all().delete()
            before_checklist.save()
            for pk_item in pk_checklist:
                result_item = BeforeInspectionResult(
                    result=request.POST[pk_item],
                    before_install_checklist_id=before_checklist,
                    before_inspection_item_id=BeforeInspectionItem.objects.get(
                        pk=pk_item
                    ),
                )
                result_item.content = request.POST[f"{pk_item}-belong"]
                result_item.save()
                if f"{pk_item}-images[]" in image_keys:
                    images = request.FILES.getlist(f"{pk_item}-images[]")
                    for img in images:
                        result_item.measures.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_before_install_checklist", type, pk)
    else:
        form = BeforeInstallCheckListForm(instance=instance)
    return render(
        request,
        "work/install/before/update_before_install_checklist.html",
        {
            "type": type,
            "checklist": instance.before_inspection_result.all(),
            "docNum": instance.pk,
            "form": form,
        },
    )
