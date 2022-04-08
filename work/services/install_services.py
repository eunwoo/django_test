from django.http import JsonResponse
from django.shortcuts import render, redirect
from system_manager.models import ConstructManager, InstallLocate
from work.forms.install_form import InstallCheckListForm
from django.contrib import messages

from work.models import (
    InspectionItem,
    InspectionResult,
    InstallCheckList,
    Measure,
)

from ..services.common_services import image_send, sms_send


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
            doing_checklist.save()
            for pk_item in pk_checklist:
                before_result_item = InspectionResult.objects.filter(
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(pk=pk_item),
                )[0]
                result_item = InspectionResult(
                    result=request.POST[pk_item],
                    install_checklist_id=doing_checklist,
                    content=request.POST[f"{pk_item}-belong"],
                    inspection_item_id=InspectionItem.objects.get(pk=pk_item),
                )
                result_item.save()
                image_ids = request.POST.getlist(f"{pk_item}-images-preloaded[]")
                for image_id in image_ids:
                    image = Measure.objects.filter(
                        pk=image_id,
                        inspectionResult=before_result_item,
                    )
                    if image:
                        image = image[0]
                        image.inspectionResult = result_item
                        image.save()
                if f"{pk_item}-images[]" in image_keys:
                    images = request.FILES.getlist(f"{pk_item}-images[]")
                    for img in images:
                        result_item.measures.create(img=img)
                before_result_item.delete()
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
    sms_send(link, [cm_phone], 3)
    checklist_ids = request.POST.getlist("checklist_id")
    message_list = []
    for checklist_id in checklist_ids:
        target = InspectionResult.objects.get(
            install_checklist_id=doc,
            inspection_item_id=InspectionItem.objects.get(pk=checklist_id),
        )
        message_list.append(
            {
                "content": target.content,
                "img": list(map(lambda x: x.img, list(target.measures.all()))),
            }
        )
    image_send(message_list, cm_phone)
    # 문자 전송 페이지 만들기


def delete_install_checklists_service(request):
    if request.method == "POST":
        install_checklist_list = request.POST.getlist("delete_list[]")
        for install_checklist in install_checklist_list:
            install_checklist = InstallCheckList.objects.get(pk=install_checklist)
            install_checklist.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)
