from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from system_manager.models import EquipmentTypes

from work.models import (
    BeforeInstallCheckList,
)

from ..services.before_install_services import (
    assign_cm,
    before_install_checklist_service,
    before_install_checklists_delete_service,
    create_item,
    get_require_users,
    measure_before_install_service,
    review_before_install_checklist_service,
    success_before_install_checklist_service,
    update_before_checklist_service,
)


@login_required(login_url="/user/login/")
def select_type(request):
    equipment_list = list(EquipmentTypes.objects.all().values_list("isActive"))
    equipment_list = list(map(lambda x: x[0], equipment_list))
    return render(
        request,
        "work/install/select_type.html",
        {"equipment_list": equipment_list},
    )


@login_required(login_url="/user/login/")
def select_install(request, type: str):
    return render(request, "work/install/select_install.html", {"type": type})


@login_required(login_url="/user/login/")
def before_install(request, type: str):
    page = request.GET.get("page", 1)

    beforeInstallItems = BeforeInstallCheckList.objects.filter(
        equipment=type,
        isSuccess=False,
    ).order_by("isCheckWriter", "-pk")

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
        assign_cm(request)
        return redirect("work:before_install", type)
    return Http404()


@login_required(login_url="/user/login/")
def delete_before_install_checklists(request):
    return before_install_checklists_delete_service(request)


@login_required(login_url="/user/login/")
def add_before_install_item(request, type):
    if request.method == "POST":
        title = request.POST.get("title")
        pk = create_item(type, title)
        return JsonResponse({"pk": pk})
    return Http404()


@login_required(login_url="/user/login/")
def review_before_install_checklist(request, type, pk):
    return review_before_install_checklist_service(request, type, pk)


@login_required(login_url="/user/login/")
def success_before_checklist(request):
    if request.method == "POST":
        return success_before_install_checklist_service(request, request.POST["pk"])
    return Http404()


def measure_before_install(request, urlcode):
    return measure_before_install_service(request, urlcode)


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
