from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..models import LocateClass, InstallLocate


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
