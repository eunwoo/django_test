from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from system_manager.models import InstallLocate
from work.forms.before_install_form import BeforeInstallCheckListForm

from work.models import (
    BeforeInspectionItem,
    BeforeInspectionResult,
    BeforeInstallCheckList,
)

from ..services.before_install_services import (
    assign_cm,
    before_install_checklist_service,
    get_require_users,
    update_before_checklist_service,
)


@login_required(login_url="/user/login/")
def select_type(request):
    return render(request, "work/install/select_type.html")


@login_required(login_url="/user/login/")
def select_install(request, type: str):
    return render(request, "work/install/select_install.html", {"type": type})


@login_required(login_url="/user/login/")
def before_install(request, type: str):
    page = request.GET.get("page", 1)

    beforeInstallItems = BeforeInstallCheckList.objects.filter(equipment=type).order_by(
        "-pk"
    )

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


@login_required(login_url="/user/login/")
def update_before_install_checklist(request, type: str, pk: int):
    return update_before_checklist_service(request, type, pk)


@login_required(login_url="/user/login/")
def get_users(request):
    users = get_require_users()
    return JsonResponse(
        {"users": list(users.values("pk", "name"))},
        json_dumps_params={"ensure_ascii": False},
    )


@login_required(login_url="/user/login/")
def required_cm(request, type):
    if request.method == "POST":
        assign_cm(request, type)
        return redirect("work:before_install", type)
    return Http404()


def read_before_checklist(request, type, pk):
    checklist = BeforeInstallCheckList.objects.get(pk=pk)
    return render(
        request,
        "work/install/before/read_checklist.html",
        {
            "checklist": checklist,
            "type": type,
        },
    )
