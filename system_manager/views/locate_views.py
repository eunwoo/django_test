from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from ..models import (
    LocateClass,
    InstallLocate,
    InstallLocateClass2,
    InstallLocateClass1,
)


@login_required(login_url="/user/login/")
def apply_locate(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    class1 = LocateClass.objects.filter(type="class1")
    class2 = LocateClass.objects.filter(type="class2")
    class3 = LocateClass.objects.filter(type="class3")
    install_locate = InstallLocate.objects.all()
    return render(
        request,
        "system_manager/apply_locate.html",
        {
            "class1": class1,
            "class2": class2,
            "class3": class3,
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
