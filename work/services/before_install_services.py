import string
import random
import datetime

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from system_manager.models import InstallLocate
from work.forms.before_install_form import BeforeInstallCheckListForm
from django.contrib import messages

from work.models import (
    BeforeInspectionItem,
    BeforeInspectionResult,
    BeforeInstallCheckList,
    BeforeMeasureImg,
)

from system_manager.models import ConstructManager

from ..services.common_services import sms_send  # , image_send


def assign_cm(request):
    doc = BeforeInstallCheckList.objects.get(pk=request.POST.get("docNum"))
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
    link = request.build_absolute_uri(
        f"/work/measure_before_install/{doc.urlCode}/",
    )
    cm_phone = cm.phone
    due_date = datetime.datetime.strptime(
        request.POST.get("expired_date"), "%Y-%m-%dT%H:%M"
    )

    sms_send(link, [cm_phone], 2, due_date.strftime("%Y년 %m월 %d일 %I:%M %p"))


def get_require_users():
    users = ConstructManager.objects.all()
    return users


def create_item(type, title):
    if type == "강관 비계":
        equipment = "1"
    elif type == "시스템 비계":
        equipment = "2"
    else:
        equipment = "3"
    new_item = BeforeInspectionItem(equipment=equipment, title=title)
    new_item.save()
    return new_item.pk


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
            before_checklist.save()
            for pk in pk_checklist:
                result_item = BeforeInspectionResult(
                    result=request.POST[pk],
                    before_install_checklist_id=before_checklist,
                    before_inspection_item_id=BeforeInspectionItem.objects.get(
                        pk=pk,
                    ),
                )
                result_item.save()
                if request.POST[pk] == "2":
                    result_measure = result_item.before_measure.create(
                        content=request.POST[f"{pk}-belong"],
                    )
                    images = request.FILES.getlist(f"{pk}-images[]")
                    for img in images:
                        result_measure.before_measure_imgs.create(img=img)
            messages.success(request, "저장이 완료되었습니다.")
            return redirect(
                "work:update_before_install_checklist",
                type,
                before_checklist.pk,
            )
    else:
        form = BeforeInstallCheckListForm()
    checklist = BeforeInspectionItem.objects.filter(
        equipment=equipment,
        init_item=True,
    )
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

            # 기본 저장 영역
            before_checklist = form.save(commit=False)
            before_checklist.equipment = type
            if "locate" in request.POST.keys():
                before_checklist.locateId = InstallLocate.objects.get(
                    pk=request.POST["locate"]
                )
            pk_checklist = request.POST.getlist("checklist-pk")
            before_checklist.save()

            # 삭제 영역
            before_list = before_checklist.before_inspection_result.all()
            for before in before_list:
                if str(before.before_inspection_item_id.pk) not in pk_checklist:
                    before.delete()

            # 수정 영역
            for pk_item in pk_checklist:
                before_result_item = BeforeInspectionResult.objects.filter(
                    before_install_checklist_id=before_checklist,
                    before_inspection_item_id=BeforeInspectionItem.objects.get(
                        pk=pk_item
                    ),
                )
                delete_before = False
                # 수정된 영역이면 해당 구문이 실행, 새로 생성된 영역은 패스
                if before_result_item:
                    before_result_item = before_result_item[0]
                    delete_before = True
                result_item = BeforeInspectionResult(
                    result=request.POST[pk_item],
                    before_install_checklist_id=before_checklist,
                    before_inspection_item_id=BeforeInspectionItem.objects.get(
                        pk=pk_item
                    ),
                )
                result_item.save()
                if request.POST[pk_item] == "2":
                    result_measure = result_item.before_measure.create(
                        content=request.POST[f"{pk_item}-belong"],
                    )
                    before_image_ids = request.POST.getlist(
                        f"{pk_item}-images-preloaded[]"
                    )
                    for before_image_id in before_image_ids:
                        before_image = BeforeMeasureImg.objects.filter(
                            pk=before_image_id,
                            beforeMeasure=before_result_item.before_measure.first(),
                        )
                        if before_image:
                            before_image = before_image[0]
                            before_image.beforeMeasure = result_measure
                            before_image.save()
                    images = request.FILES.getlist(f"{pk_item}-images[]")
                    for img in images:
                        result_measure.before_measure_imgs.create(img=img)
                if delete_before:
                    before_result_item.delete()
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


def before_install_checklists_delete_service(request):
    if request.method == "POST":
        before_install_checklist_list = request.POST.getlist("delete_list[]")
        for before_install_checklist in before_install_checklist_list:
            before_install_checklist = BeforeInstallCheckList.objects.get(
                pk=before_install_checklist
            )
            before_install_checklist.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)


def review_before_install_checklist_service(request, type, pk):
    checklist = BeforeInstallCheckList.objects.get(pk=pk)
    isSave = False
    inspectionResults = checklist.before_inspection_result.filter(result="2")
    for inspectionResult in inspectionResults:
        if not inspectionResult.before_measure.last().isCM:
            isSave = True
            break
    if request.method == "POST":
        for inspectionResult in inspectionResults:
            lastMeasure = inspectionResult.before_measure.last()
            if f"{inspectionResult.pk}-content" in request.POST.keys():
                if lastMeasure.isCM:
                    newMeasure = inspectionResult.before_measure.create(
                        content=request.POST[f"{inspectionResult.pk}-content"],
                    )
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        newMeasure.before_measure_imgs.create(img=img)
                else:
                    lastMeasure.content = request.POST[f"{inspectionResult.pk}-content"]
                    lastMeasure.save()
                    before_images = list(
                        request.POST.getlist(
                            f"{inspectionResult.pk}-images-preloaded[]"
                        )
                    )
                    for measure_img in lastMeasure.before_measure_imgs.all():
                        if str(measure_img.pk) not in before_images:
                            measure_img.delete()
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        lastMeasure.before_measure_imgs.create(img=img)
        messages.success(request, "저장이 완료되었습니다.")
        isSave = True
    return render(
        request,
        "work/install/before/review_before_install_checklist.html",
        {
            "type": type,
            "checklist": checklist,
            "isSave": isSave,
        },
    )


def measure_before_install_service(request, urlCode):
    checklist = get_object_or_404(
        BeforeInstallCheckList,
        urlCode=urlCode,
        isCheckWriter=True,
    )
    if checklist.expired_date < timezone.now():
        return redirect("main:home")
    isSave = False
    if request.method == "POST":
        inspectionResults = checklist.before_inspection_result.filter(result="2")
        for inspectionResult in inspectionResults:
            lastMeasure = inspectionResult.before_measure.last()
            if f"{inspectionResult.pk}-content" in request.POST.keys():
                if not lastMeasure.isCM:
                    newMeasure = inspectionResult.before_measure.create(
                        content=request.POST[f"{inspectionResult.pk}-content"],
                        isCM=True,
                        cm=checklist.cm,
                    )
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        newMeasure.before_measure_imgs.create(img=img)
                else:
                    lastMeasure.content = request.POST[f"{inspectionResult.pk}-content"]
                    lastMeasure.save()
                    before_images = list(
                        request.POST.getlist(
                            f"{inspectionResult.pk}-images-preloaded[]"
                        )
                    )
                    for measure_img in lastMeasure.before_measure_imgs.all():
                        if str(measure_img.pk) not in before_images:
                            measure_img.delete()
                    images = request.FILES.getlist(f"{inspectionResult.pk}-images[]")
                    for img in images:
                        lastMeasure.before_measure_imgs.create(img=img)
        messages.success(request, "저장이 완료되었습니다.")
        isSave = True
    return render(
        request,
        "work/install/before/measure_checklist.html",
        {
            "checklist": checklist,
            "isSave": isSave,
        },
    )


def measure_apply_before_install(request, urlCode):
    checklist = get_object_or_404(
        BeforeInstallCheckList,
        urlCode=urlCode,
        isCheckWriter=True,
    )
    checklist.isCheckCM = True
    checklist.isCheckWriter = False
    checklist.save()
    return redirect("main:home")


def success_before_install_checklist_service(request, pk):
    checklist = get_object_or_404(BeforeInstallCheckList, pk=pk)
    checklist.isSuccess = True
    checklist.isCheckCM = True
    checklist.isCheckWriter = True
    link = request.build_absolute_uri(
        f"/work/read_before_install/{checklist.equipment}/{pk}",
    )
    sms_send(link, [checklist.cm.phone], 4)
    checklist.save()
    return JsonResponse({"result": "success"})
