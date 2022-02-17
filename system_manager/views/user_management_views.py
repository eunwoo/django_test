from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.models import CustomUser


@login_required(login_url="/user/login/")
def user_management(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    await_users = CustomUser.objects.filter(is_system_manager=False, register=False)
    registered_users = CustomUser.objects.filter(is_system_manager=False, register=True)
    return render(
        request,
        "system_manager/user_management.html",
        {"await_users": await_users, "registered_users": registered_users},
    )


@login_required(login_url="/user/login/")
def delete_user(request, pk):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return redirect("system_manager:user_management")
    return redirect("main:home")


@login_required(login_url="/user/login/")
def register_user(request, pk):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    if request.method == "POST":
        user = CustomUser.objects.get(pk=pk)
        user.register = True
        user.save()
        return redirect("system_manager:user_management")
    return redirect("main:home")
