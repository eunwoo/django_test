from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..models import EquipmentTypes
from ..forms import FieldForm


@login_required(login_url="/user/login/")
def apply_field(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    form = FieldForm()
    equipments = EquipmentTypes.objects.all()
    return render(
        request,
        "system_manager/apply_field.html",
        {"form": form, "equipments": equipments},
    )
