from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from work.models import MaterialSupplyReport
from work.services.common_services import assign_user

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
        doc = MaterialSupplyReport.objects.get(docNum=request.POST.get("docNum"))
        base_link = (
            "/work/update_material/"
            if request.user.class2 != "총괄 건설사업관리기술인"
            else "/work/read_material/"
        )
        link = request.build_absolute_uri(base_link + str(doc.docNum))
        assign_user(
            request.user,
            doc,
            int(request.POST.get("sign", 1)),
            link,
        )
        return redirect("work:material")
    return Http404("잘못된 접근입니다.")


@login_required(login_url="/user/login/")
def read_material(request, pk):
    material = read_material_service(request.user, pk)
    material_url = list(map(lambda x: x.file.url, material.material_docs.all()))
    return render(
        request,
        "work/material/read_material.html",
        {"material": material, "material_url": material_url},
    )


@login_required(login_url="/user/login/")
def delete_material(request, pk):
    pass
