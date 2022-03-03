from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers

from ..models import (
    InstallLocate,
    InstallLocateClass2,
    InstallLocateClass1,
)


@login_required(login_url="/user/login/")
def apply_locate(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    class1 = InstallLocateClass1.objects.all()
    install_locate = InstallLocate.objects.all()
    return render(
        request,
        "system_manager/apply_locate.html",
        {
            "class1": class1,
            "install_locate": install_locate,
        },
    )


@login_required(login_url="/user/login/")
def locate_class(request, pk):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return redirect("main:home")


@login_required(login_url="/user/login/")
def read_locate_class(request, class_type):
    class_id = request.GET.get("class_id", 1)
    if class_type == 1:
        install_locate = InstallLocateClass1.objects.all()
    elif class_type == 2:
        install_locate = InstallLocateClass2.objects.filter(
            class1=InstallLocateClass1.objects.get(pk=class_id)
        )
    elif class_type == 3:
        install_locate = InstallLocate.objects.filter(
            class2=InstallLocateClass2.objects.get(pk=class_id)
        )
    else:
        return Http404()
    return JsonResponse(
        {"install_locate": list(install_locate.values())},
        json_dumps_params={"ensure_ascii": False},
    )


@login_required(login_url="/user/login/")
def add_locate(request):
    if request.method == "POST":
        class_type = int(request.POST.get("class_type"))
        if class_type == 1:
            target_class = InstallLocateClass1(
                class1=request.POST.get("name"),
            )
            target_class.save()
        elif class_type == 2:
            target_class = InstallLocateClass2(
                class2=request.POST.get("name"),
                class1=InstallLocateClass1.objects.get(pk=request.POST.get("class_id")),
            )
            target_class.save()
        elif class_type == 3:
            target_class = InstallLocate(
                class3=request.POST.get("name"),
                class2=InstallLocateClass2.objects.get(pk=request.POST.get("class_id")),
            )
            target_class.save()
        return JsonResponse(
            {"result": "success", "data": serializers.serialize("json", [target_class])}
        )
    else:
        return Http404()


@login_required(login_url="/user/login/")
def delete_locate(request):
    if request.method == "POST":
        class_type = int(request.POST.get("class_type"))
        if class_type == 1:
            InstallLocateClass1.objects.get(pk=request.POST.get("class_id")).delete()
        elif class_type == 2:
            InstallLocateClass2.objects.get(pk=request.POST.get("class_id")).delete()
        elif class_type == 3:
            InstallLocate.objects.get(pk=request.POST.get("class_id")).delete()
        return HttpResponse(status=200)
    return Http404()
