from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from system_manager.models import DocsFile
from work.utils.send_alert import email_send

from ..models import MaterialSupplyReport, SupplyList
from ..forms.material_forms import (
    GeneralEngineerMaterialSupplyReportForm,
    GeneralManagerMaterialSupplyReportForm,
)


def get_material_list_by_user(user):
    if user.class2 == "일반 관리자":
        return MaterialSupplyReport.objects.filter(writerId=user).order_by(
            "-isCheckManager", "-docNum"
        )
    elif user.class2 == "현장 대리인":
        return MaterialSupplyReport.objects.filter(agentId=user).order_by(
            "-isReadAgent", "-isCheckAgent", "-docNum"
        )
    elif user.class2 == "일반 건설사업관리기술인":
        return MaterialSupplyReport.objects.filter(generalEngineerId=user).order_by(
            "-isReadGeneralEngineer", "-isCheckGeneralEngineer", "-docNum"
        )
    else:
        return MaterialSupplyReport.objects.filter(totalEngineerId=user).order_by(
            "-isReadTotalEngineer", "-isSuccess", "-docNum"
        )


def create_material_service(request):
    if request.method == "POST":
        form = GeneralManagerMaterialSupplyReportForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.writerId = request.user
            files = request.POST.getlist("docs[]")
            supply_comp = request.POST.getlist("supply_comp[]")
            supply_type = request.POST.getlist("supply_type[]")
            supply_size = request.POST.getlist("supply_size[]")
            supply_etc = request.POST.getlist("supply_etc[]")
            material.save()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                material.docs.add(doc_file)
            for index in range(len(supply_comp)):
                supply_list = SupplyList.objects.create(
                    name=supply_comp[index],
                    goods=supply_type[index],
                    size=supply_size[index],
                    etc=supply_etc[index],
                    materialSupplyReportId=material,
                )
                supply_list.save()
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
        {"form": form, "docNum": docNum, "accept_docs": accept_docs},
    )


def update_material_service(request, docNum):
    if request.user.class2 == "일반 관리자":
        return update_material_general(request, docNum)
    elif request.user.class2 == "현장 대리인":
        return update_material_agent(request, docNum)
    elif request.user.class2 == "일반 건설사업관리기술인":
        return update_material_generalEngineer(request, docNum)
    else:
        return Http404()


def update_material_agent(request, docNum):
    material = MaterialSupplyReport.objects.get(docNum=docNum)
    return render(
        request, "work/material/update_material_agent.html", {"material": material}
    )


def update_material_generalEngineer(request, docNum):
    material = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralEngineerMaterialSupplyReportForm(request.POST, instance=material)
        if form.is_valid():
            material = form.save()
            return redirect("work:update_material", material.docNum)
    else:
        form = GeneralEngineerMaterialSupplyReportForm(instance=material)
    return render(
        request,
        "work/material/update_material_generalEngineer.html",
        {"material": material, "form": form},
    )


def update_material_general(request, docNum):
    instance = MaterialSupplyReport.objects.get(docNum=docNum)
    if request.method == "POST":
        form = GeneralManagerMaterialSupplyReportForm(request.POST, instance=instance)
        if form.is_valid():
            material = form.save(commit=False)
            material.writerId = request.user
            files = request.POST.getlist("docs[]")
            supply_comp = request.POST.getlist("supply_comp[]")
            supply_type = request.POST.getlist("supply_type[]")
            supply_size = request.POST.getlist("supply_size[]")
            supply_etc = request.POST.getlist("supply_etc[]")
            material.save()
            material.docs.clear()
            material.supply_list.clear()
            for file_id in files:
                doc_file = DocsFile.objects.get(pk=int(file_id))
                material.docs.add(doc_file)
            for index in range(len(supply_comp)):
                supply_list = SupplyList.objects.create(
                    name=supply_comp[index],
                    goods=supply_type[index],
                    size=supply_size[index],
                    etc=supply_etc[index],
                )
                supply_list.save()
                material.supply_list.add(supply_list)
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
        },
    )


def read_material_service(user, pk):
    material = MaterialSupplyReport.objects.get(docNum=pk)
    if user.class2 == "일반 관리자":
        material.isCheckManager = True
    elif user.class2 == "현장 대리인":
        material.isCheckAgent = True
    elif user.class2 == "일반 건설사업관리기술인":
        material.isCheckGeneralEngineer = True
    material.save()
    return material
