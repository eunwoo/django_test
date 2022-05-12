from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from work.models import InstallCheckList
from ..services.install_services import (
    assign_cm,
    create_item,
    delete_install_checklists_service,
    install_checklist_service,
    measure_install_service,
    review_install_checklist_service,
    success_install_checklist_service,
    update_checklist_service,
)


@login_required(login_url="/user/login/")
def install(request, type: str):
    page = request.GET.get("page", 1)

    beforeInstallItems = InstallCheckList.objects.filter(
        equipment=type,
        isSuccess=False,
    ).order_by("isCheckWriter", "-pk")

    paginator = Paginator(beforeInstallItems, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "work/install/doing/install.html",
        {
            "type": type,
            "InstallItems": page_obj,
        },
    )


@login_required(login_url="/user/login/")
def install_checklist(request, type: str):
    return install_checklist_service(request, type)


@login_required(login_url="/user/login/")
def update_install_checklist(request, type: str, pk: int):
    return update_checklist_service(request, type, pk)


@login_required(login_url="/user/login/")
def required_cm(request, type):
    if request.method == "POST":
        assign_cm(request, type)
        return redirect("work:install", type)
    return Http404()


@login_required(login_url="/user/login/")
def delete_install_checklists(request):
    return delete_install_checklists_service(request)


@login_required(login_url="/user/login/")
def add_install_item(request, type):
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        pk = create_item(type, title, category)
        return JsonResponse({"pk": pk})
    return Http404()


@login_required(login_url="/user/login/")
def review_install_checklist(request, type, pk):
    return review_install_checklist_service(request, type, pk)


@login_required(login_url="/user/login/")
def success_install_checklist(request):
    if request.method == "POST":
        return success_install_checklist_service(request.POST["pk"])
    return Http404()


def read_checklist(request, type, pk):
    checklist = InstallCheckList.objects.get(pk=pk)
    return render(
        request,
        "work/install/doing/read_checklist.html",
        {
            "checklist": checklist,
            "checklist_items": checklist.inspection_result.all(),
            "type": type,
        },
    )


def measure_install(request, urlcode):
    return measure_install_service(request, urlcode)
