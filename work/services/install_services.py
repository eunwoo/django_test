import random
import string
import datetime

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from system_manager.models import ConstructManager, InstallLocate
from work.forms.install_form import InstallCheckListForm
from django.contrib import messages

from work.models import (
    InspectionItem,
    InspectionItemCategory,
    InspectionResult,
    InstallCheckList,
    MeasureImg,
)

from ..services.common_services import sms_send


def create_item(type, title, category):
    if type == "강관 비계":
        equipment = "1"
    elif type == "시스템 비계":
        equipment = "2"
    else:
        equipment = "3"
    new_item = InspectionItem(
        equipment=equipment,
        title=title,
        categoryId=InspectionItemCategory.objects.get(type=category),
    )
    new_item.save()
    return new_item.pk


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
            doing_checklist.save()
            for pk in pk_checklist:
                result_item = InspectionResult(
                    result=request.POST[pk],
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(pk=pk),
                )
                result_item.save()
                if request.POST[pk] == "2":
                    result_measure = result_item.measure.create(
                        content=request.POST[f"{pk}-belong"]
                    )
                    images = request.FILES.getlist(f"{pk}-images[]")
                    for img in images:
                        result_measure.measure_imgs.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect(
                "work:update_install_checklist",
                type,
                doing_checklist.pk,
            )
    else:
        form = InstallCheckListForm()
    checklist = InspectionItem.objects.filter(
        equipment=equipment,
        init_item=True,
    ).order_by("categoryId__pk")
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
            # 기본 저장 영역
            doing_checklist = form.save(commit=False)
            doing_checklist.equipment = type
            if "locate" in request.POST.keys():
                doing_checklist.locateId = InstallLocate.objects.get(
                    pk=request.POST["locate"]
                )
            pk_checklist = request.POST.getlist("checklist-pk")
            doing_checklist.save()

            # 삭제 영역
            install_list = doing_checklist.inspection_result.all()
            for install in install_list:
                if str(install.inspection_item_id.pk) not in pk_checklist:
                    install.delete()

            # 수정 영역
            for pk_item in pk_checklist:
                before_result_item = InspectionResult.objects.filter(
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(
                        pk=pk_item,
                    ),
                )
                delete_before = False
                # 수정된 영역이면 해당 구문이 실행, 새로 생성된 영역은 패스
                if before_result_item:
                    before_result_item = before_result_item[0]
                    delete_before = True
                result_item = InspectionResult(
                    result=request.POST[pk_item],
                    install_checklist_id=doing_checklist,
                    inspection_item_id=InspectionItem.objects.get(pk=pk_item),
                )
                result_item.save()
                if request.POST[pk_item] == "2":
                    result_measure = result_item.measure.create(
                        content=request.POST[f"{pk_item}-belong"]
                    )
                    before_image_ids = request.POST.getlist(
                        f"{pk_item}-images-preloaded[]"
                    )
                    for before_image_id in before_image_ids:
                        before_image = MeasureImg.objects.get(
                            pk=before_image_id,
                        )
                        if before_image:
                            before_image.measure = result_measure
                            before_image.save()
                    images = request.FILES.getlist(f"{pk_item}-images[]")
                    for img in images:
                        result_measure.measure_imgs.create(img=img)
                if delete_before:
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
    doc = InstallCheckList.objects.get(pk=request.POST.get("docNum"))
    doc.isCheckWriter = True
    doc.isCheckCM = False
    if not doc.cm:
        cm = ConstructManager.objects.get(pk=request.POST.get("sign"))
        doc.cm = cm
    else:
        cm = doc.cm
    doc.expired_date = request.POST.get("expired_date")
    doc.urlCode = "".join(
        random.choices(
            string.ascii_letters + string.digits,
            k=12,
        )
    )
    doc.save()
    link = request.build_absolute_uri(f"/work/measure_install/{doc.urlCode}")
    cm_phone = cm.phone
    due_date = datetime.datetime.strptime(
        request.POST.get("expired_date"), "%Y-%m-%dT%H:%M"
    )

    sms_send(link, [cm_phone], 3, due_date.strftime("%Y년 %m월 %d일 %I:%M %p"))


def delete_install_checklists_service(request):
    if request.method == "POST":
        install_checklist_list = request.POST.getlist("delete_list[]")
        for install_checklist in install_checklist_list:
            install_checklist = InstallCheckList.objects.get(
                pk=install_checklist,
            )
            install_checklist.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)


def measure_install_service(request, urlCode):
    checklist = get_object_or_404(
        InstallCheckList,
        urlCode=urlCode,
        isCheckWriter=True,
    )
    if request.method == "POST":
        form_key = list(request.POST.keys())
        form_key.remove("csrfmiddlewaretoken")
        for key in form_key:
            pk = key.split("-")[0]
            inspection_result = InspectionResult.objects.get(pk=pk)
            measure = inspection_result.measure.create(
                isCM=True,
                content=request.POST[key],
                cm=checklist.cm,
            )
            for image in request.FILES.getlist(pk + "-images[]"):
                measure.measure_imgs.create(img=image)
        checklist.isCheckCM = True
        checklist.isCheckWriter = False
        checklist.save()
        return redirect("main:home")
    if checklist.expired_date < timezone.now():
        return redirect("main:home")
    return render(
        request,
        "work/install/doing/measure_checklist.html",
        {
            "checklist": checklist,
            "checklist_items": checklist.inspection_result.all(),
        },
    )


def review_install_checklist_service(request, type, pk):
    checklist = InstallCheckList.objects.get(pk=pk)
    isSave = False
    inspectionResults = checklist.inspection_result.filter(result="2")
    for inspectionResult in inspectionResults:
        if not inspectionResult.measure.last().isCM:
            isSave = True
            break
    if request.method == "POST":
        for inspectionResult in inspectionResults:
            lastMeasure = inspectionResult.measure.last()
            if f"{inspectionResult.pk}-belong" in request.POST.keys():
                if lastMeasure.isCM:
                    newMeasure = inspectionResult.measure.create(
                        content=request.POST[f"{inspectionResult.pk}-content"],
                    )
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        newMeasure.measure_imgs.create(img=img)
                else:
                    lastMeasure.content = request.POST[f"{inspectionResult.pk}-content"]
                    lastMeasure.save()
                    before_images = list(
                        request.POST.getlist(
                            f"{inspectionResult.pk}-images-preloaded[]"
                        )
                    )
                    for measure_img in lastMeasure.measure_imgs.all():
                        if str(measure_img.pk) not in before_images:
                            measure_img.delete()
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        lastMeasure.measure_imgs.create(img=img)
        messages.success(request, "저장이 완료되었습니다.")
        isSave = True
    return render(
        request,
        "work/install/doing/review_install_checklist.html",
        {
            "type": type,
            "checklist": checklist,
            "checklist_items": checklist.inspection_result.all(),
            "isSave": isSave,
        },
    )


def success_install_checklist_service(request, pk):
    checklist = get_object_or_404(InstallCheckList, pk=pk)
    checklist.isSuccess = True
    checklist.isCheckCM = True
    checklist.isCheckWriter = True
    link = request.build_absolute_uri(
        f"/work/read_install/{checklist.equipment}/{pk}",
    )
    sms_send(link, [checklist.cm.phone], 5)
    checklist.save()
    return JsonResponse({"result": "success"})
