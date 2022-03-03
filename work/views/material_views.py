from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import MaterialSupplyReport
from work.services.common_services import assign_user

from work.utils.send_alert import email_send

from ..services.material_services import (
    create_material_service,
    get_material_list_by_user,
    read_material_service,
    update_material_service,
)


@login_required(login_url="/user/login/")
def material(request):
    page = request.GET.get("page", 1)

    material_list = get_material_list_by_user(request.user)

    paginator = Paginator(material_list, 10)
    page_obj = paginator.get_page(page)

    return render(request, "work/material/material.html", {"materialitems": page_obj})


@login_required(login_url="/user/login/")
def create_material(request):
    return create_material_service(request)


@login_required(login_url="/user/login/")
def update_material(request, pk):
    return update_material_service(request, pk)


@login_required(login_url="/user/login/")
def require_sign_material(request):
    if request.method == "POST":
        email_send(int(request.POST.get("sign")))
        doc = MaterialSupplyReport.objects.get(docNum=request.POST.get("docNum"))
        assign_user(request.user, doc, int(request.POST.get("sign", 1)))
        return redirect("work:material")
    return Http404("잘못된 접근입니다.")


@login_required(login_url="/user/login/")
def read_material(request, pk):
    material = read_material_service(request.user, pk)
    return render(
        request,
        "work/material/read_material.html",
        {"material": material},
    )


@login_required(login_url="/user/login/")
def delete_material(request, pk):
    pass
