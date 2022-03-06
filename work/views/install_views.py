from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from system_manager.models import InstallLocate
from work.forms.before_install_form import BeforeInstallCheckListForm

from work.models import (
    BeforeInspectionItem,
    BeforeInspectionResult,
    BeforeInstallCheckList,
)

from ..services.before_install_services import before_install_checklist_service


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
    return before_install_checklist_service(request, type)
