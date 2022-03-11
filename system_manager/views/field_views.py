from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..models import EquipmentTypes, ConstructManager, Field
from ..forms import FieldForm, CmPhoneForm


@login_required(login_url="/user/login/")
def manage_field(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/manage_field.html")


@login_required(login_url="/user/login/")
def apply_field(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        if Field.objects.all().count() == 0:
            form = FieldForm(request.POST)
        else:
            form = FieldForm(request.POST, instance=Field.objects.get(id=1))
        if form.is_valid():
            form.save()
            return redirect("system_manager:manage_field")
    # 현장이 없을 경우 새로 등록, 있을 경우 수정모드
    if Field.objects.all().count() == 0:
        form = FieldForm()
    else:
        form = FieldForm(instance=Field.objects.get(id=1))
    return render(
        request,
        "system_manager/apply_field.html",
        {"form": form},
    )


@login_required(login_url="/user/login/")
def manage_equipments(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    equipments = EquipmentTypes.objects.all()
    return render(
        request,
        "system_manager/manage_equipments.html",
        {"equipments": equipments},
    )


@login_required(login_url="/user/login/")
def manage_cm_calls(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        form = CmPhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("system_manager:manage_cm_calls")
    cm_calls = ConstructManager.objects.all()
    return render(
        request,
        "system_manager/manage_cm_calls.html",
        {"cm_calls": cm_calls},
    )


@login_required(login_url="/user/login/")
def delete_cm_calls(request, pk):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        user = ConstructManager.objects.get(pk=pk)
        user.delete()
        return redirect("system_manager:manage_cm_calls")
    return redirect("main:home")


@login_required(login_url="/user/login/")
def apply_equipments(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        equipment_list = EquipmentTypes.objects.all().values_list("type", flat=True)
        print(request.POST.keys())
        for equipment in equipment_list:
            if equipment in request.POST.keys():
                target = EquipmentTypes.objects.get(type=equipment)
                target.isActive = True
                target.save()
            else:
                target = EquipmentTypes.objects.get(type=equipment)
                target.isActive = False
                target.save()
        return redirect("system_manager:manage_field")
    return redirect("main:home")
