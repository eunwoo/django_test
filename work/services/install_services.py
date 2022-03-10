from django.shortcuts import render, redirect
from system_manager.models import ConstructManager, InstallLocate
from work.forms.install_form import InstallCheckListForm
from django.contrib import messages

from work.models import (
    InspectionItem,
    InspectionResult,
    InstallCheckList,
)

from ..services.common_services import sms_send


def install_checklist_service(request, type: str):
    equipment = ""
    if type == "강관 비계":
        equipment = "1"
    elif type == "시스템 비계":
        equipment = "2"
    else:
        equipment = "3"
    if request.method == "POST":
        form = InstallCheckListForm(request.POST)
        if form.is_valid():
            doing_checklist = form.save(commit=False)
            doing_checklist.equipment = type
            doing_checklist.writerId = request.user
            doing_checklist.locateId = InstallLocate.objects.get(
                pk=request.POST["locate"]
            )
            pk_checklist = request.POST.getlist("checklist-pk")
            image_keys = request.FILES.keys()
            doing_checklist.save()
            for pk in pk_checklist:
                result_item = InspectionResult(
                    result=request.POST[pk],
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(pk=pk),
                )
                result_item.content = request.POST[f"{pk}-belong"]
                result_item.save()
                if f"{pk}-images[]" in image_keys:
                    images = request.FILES.getlist(f"{pk}-images[]")
                    for img in images:
                        result_item.measures.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect(
                "work:update_install_checklist",
                type,
                doing_checklist.pk,
            )
    else:
        form = InstallCheckListForm()
    checklist = InspectionItem.objects.filter(equipment=equipment).order_by(
        "categoryId__pk"
    )
    last_doc = InstallCheckList.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.pk + 1
    return render(
        request,
        "work/install/doing/install_checklist.html",
        {
            "type": type,
            "checklist": checklist,
            "docNum": docNum,
            "form": form,
        },
    )


def update_checklist_service(request, type, pk):
    instance = InstallCheckList.objects.get(pk=pk)
    if request.method == "POST":
        form = InstallCheckListForm(request.POST, instance=instance)
        if form.is_valid():
            doing_checklist = form.save(commit=False)
            doing_checklist.equipment = type
            if "locate" in request.POST.keys():
                doing_checklist.locateId = InstallLocate.objects.get(
                    pk=request.POST["locate"]
                )
            pk_checklist = request.POST.getlist("checklist-pk")
            image_keys = request.FILES.keys()
            doing_checklist.inspection_result.all().delete()
            doing_checklist.save()
            for pk_item in pk_checklist:
                result_item = InspectionResult(
                    result=request.POST[pk_item],
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(pk=pk_item),
                )
                result_item.content = request.POST[f"{pk_item}-belong"]
                result_item.save()
                if f"{pk_item}-images[]" in image_keys:
                    images = request.FILES.getlist(f"{pk_item}-images[]")
                    for img in images:
                        result_item.measures.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_install_checklist", type, pk)
    else:
        form = InstallCheckListForm(instance=instance)
    return render(
        request,
        "work/install/doing/update_install_checklist.html",
        {
            "type": type,
            "checklist": instance.inspection_result.all(),
            "docNum": instance.pk,
            "form": form,
        },
    )


def assign_cm(request, type):
    cm = ConstructManager.objects.get(pk=request.POST.get("sign"))
    doc = InstallCheckList.objects.get(pk=request.POST.get("docNum"))
    doc.isSuccess = True
    doc.save()
    link = request.build_absolute_uri(f"/work/read_install/{type}/{doc.pk}/")
    cm_phone = cm.phone
    sms_send(link, [cm_phone])
    # 문자 전송 페이지 만들기
