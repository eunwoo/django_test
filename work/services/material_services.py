from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from system_manager.models import DocsFile, Field

from ..models import MaterialSupplyReport, SupplyList, MaterialDocs
from ..forms.material_forms import (
    GeneralEngineerMaterialSupplyReportForm,
    GeneralManagerMaterialSupplyReportForm,
    TotalEngineerMaterialSupplyReportForm,
)
from django.contrib import messages


# 유저별로 자재 공급원 신고서 목록 로드
def get_material_list_by_user(user):
    if user.class2 == "일반 사용자":
        return MaterialSupplyReport.objects.filter(
            writerId=user,
            isSuccess=False,
        ).order_by(
            "isCheckManager",
            "-docNum",
        )
    elif user.class2 == "현장 대리인":
        return MaterialSupplyReport.objects.filter(
            agentId=user,
            isSuccess=False,
        ).order_by(
            "isCheckAgent",
            "-docNum",
        )
    elif user.class2 == "일반 건설사업관리기술인":
        return MaterialSupplyReport.objects.filter(
            generalEngineerId=user,
            isSuccess=False,
        ).order_by(
            "isCheckGeneralEngineer",
            "-docNum",
        )
    else:
        return MaterialSupplyReport.objects.filter(
            totalEngineerId=user,
            isSuccess=False,
        ).order_by(
            "-docNum",
        )


# 자재 공급원 신고서 작성
def create_material_service(request):
    field = Field.objects.get(pk=1)
    if request.method == "POST":
        form = GeneralManagerMaterialSupplyReportForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.writerId = request.user
            files = request.POST.getlist("docs[]")
            supply_comp = request.POST.getlist("supply_comp[]")
            supply_type = request.POST.getlist("supply_type[]")
            supply_size = request.POST.getlist("supply_size[]")
            supply_amount = request.POST.getlist("supply_amount[]")
            supply_etc = request.POST.getlist("supply_etc[]")
            material.fieldId = field
            material.isSaveManager = True
            material.save()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                material.docs.add(doc_file)
            for index in range(len(supply_comp)):
                supply_list = SupplyList.objects.create(
                    name=supply_comp[index],
                    goods=supply_type[index],
                    size=supply_size[index],
                    amount=supply_amount[index],
                    etc=supply_etc[index],
                    materialSupplyReportId=material,
                )
                supply_list.save()
            file_id_list = [
                "businessLicenses",
                "deliveryPerformanceCertificate",
                "safetyCertificate",
                "qualityTestReport",
                "testPerformanceComparisonTable",
            ]
            for file_id in file_id_list:
                if file_id not in request.FILES:
                    continue
                for file in request.FILES.getlist(file_id):
                    material.material_docs.create(
                        file=file,
                        filename=file.name,
                        type=file_id,
                    )
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_material", material.docNum)
    else:
        form = GeneralManagerMaterialSupplyReportForm()
    last_doc = MaterialSupplyReport.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1
    accept_docs = DocsFile.objects.filter(type="가설기자재 공급원 승인 문서")
    return render(
        request,
        "work/material/create_material.html",
        {
            "form": form,
            "docNum": docNum,
            "accept_docs": accept_docs,
            "field": field,
        },
    )


# 자재 공급원 신고서 수정
def update_material_service(request, docNum):
    if request.user.class2 == "일반 사용자":
        return update_material_general(request, docNum)
    elif request.user.class2 == "현장 대리인":
        return update_material_agent(request, docNum)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_material_generalEngineer(request, docNum)
    elif request.user.class2 == "총괄 건설사업관리기술인":
        return update_material_totalEngineer(request, docNum)
    else:
        return Http404()


# 일반관리자 자재 공급원 신고서 작성
def update_material_general(request, docNum):
    instance = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralManagerMaterialSupplyReportForm(
            request.POST,
            request.FILES,
            instance=instance,
        )
        if form.is_valid():
            material = form.save(commit=False)
            material.writerId = request.user
            files = request.POST.getlist("docs[]")
            supply_comp = request.POST.getlist("supply_comp[]")
            supply_type = request.POST.getlist("supply_type[]")
            supply_size = request.POST.getlist("supply_size[]")
            supply_amount = request.POST.getlist("supply_amount[]")
            supply_etc = request.POST.getlist("supply_etc[]")
            material.save()
            if files:
                material.docs.clear()
            material.supply_list.all().delete()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                material.docs.add(doc_file)
            for index in range(len(supply_comp)):
                supply_list = SupplyList.objects.create(
                    name=supply_comp[index],
                    goods=supply_type[index],
                    size=supply_size[index],
                    amount=supply_amount[index],
                    etc=supply_etc[index],
                    materialSupplyReportId=material,
                )
                supply_list.save()
                material.supply_list.add(supply_list)
            file_id_list = [
                "businessLicenses",
                "deliveryPerformanceCertificate",
                "safetyCertificate",
                "qualityTestReport",
                "testPerformanceComparisonTable",
            ]
            for file_id in file_id_list:
                if file_id not in request.FILES:
                    continue
                MaterialDocs.objects.filter(
                    type=file_id, materialSupplyReport=material
                ).delete()
                for file in request.FILES.getlist(file_id):
                    material.material_docs.create(
                        file=file,
                        filename=file.name,
                        type=file_id,
                    )
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_material", material.docNum)
    else:
        form = GeneralManagerMaterialSupplyReportForm(instance=instance)
    accept_docs = DocsFile.objects.filter(type="가설기자재 공급원 승인 문서")
    supply_origins = instance.supply_list.all()
    return render(
        request,
        "work/material/create_material.html",
        {
            "form": form,
            "docNum": docNum,
            "material": instance,
            "accept_docs": accept_docs,
            "supply_origins": supply_origins,
            "field": instance.fieldId,
        },
    )


# 현장대리인 자재 공급원 신고서 작성
def update_material_agent(request, docNum):
    material = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        material.isSaveAgent = True
        material.save()
        messages.success(request, "저장이 완료되었습니다.")
    return render(
        request,
        "work/material/update_material_agent.html",
        {"material": material},
    )


# 일반 건설사업관리기술인 자재 공급원 신고서 작성
def update_material_generalEngineer(request, docNum):
    material = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralEngineerMaterialSupplyReportForm(
            request.POST,
            instance=material,
        )
        if form.is_valid():
            material = form.save(commit=False)
            material.isSaveGeneralEngineer = True
            material.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_material", material.docNum)
        else:
            print(form.errors)
    else:
        form = GeneralEngineerMaterialSupplyReportForm(instance=material)
    return render(
        request,
        "work/material/update_material_generalEngineer.html",
        {"material": material, "form": form},
    )


# 총괄 건설사업관리기술인 자재 공급원 신고서 작성
def update_material_totalEngineer(request, docNum):
    material = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        form = TotalEngineerMaterialSupplyReportForm(
            request.POST,
            instance=material,
        )
        if form.is_valid():
            material = form.save(commit=False)
            material.isSaveTotalEngineer = True
            material.save()
            messages.success(request, "저장이 완료되었습니다.")
            return redirect("work:update_material", material.docNum)
    else:
        form = TotalEngineerMaterialSupplyReportForm(instance=material)
    return render(
        request,
        "work/material/update_material_totalEngineer.html",
        {"material": material, "form": form},
    )


# 자재 공급원 신고서 조회
def read_material_service(pk):
    material = MaterialSupplyReport.objects.get(docNum=pk)
    return material


# 자재 공급원 신고서 삭제
def delete_materials_service(request):
    if request.method == "POST":
        safety_list = request.POST.getlist("delete_list[]")
        for safety in safety_list:
            safety = MaterialSupplyReport.objects.get(docNum=safety)
            safety.delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)
