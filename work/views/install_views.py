from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator

from work.models import BeforeInspectionItem, BeforeInstallCheckList


@login_required(login_url="/user/login/")
def select_type(request):
    return render(request, "work/install/select_type.html")


@login_required(login_url="/user/login/")
def select_install(request, type: str):
    return render(request, "work/install/select_install.html", {"type": type})


@login_required(login_url="/user/login/")
def before_install(request, type: str):
    page = request.GET.get("page", 1)

    beforeInstallItems = BeforeInstallCheckList.objects.filter(equipment=type)

    paginator = Paginator(beforeInstallItems, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "work/install/before/before_install.html",
        {
            "type": type,
            "beforeInstallItems": page_obj,
        },
    )


@login_required(login_url="/user/login/")
def before_install_checklist(request, type: str):
    equipment = ""
    if type == "강관 비계":
        equipment = "1"
    elif type == "시스템 비계":
        equipment = "2"
    else:
        equipment = "3"
    checklist = BeforeInspectionItem.objects.filter(equipment=equipment)
    return render(
        request,
        "work/install/before/before_install_checklist.html",
        {
            "type": type,
            "checklist": checklist,
        },
    )
