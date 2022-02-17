from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def apply_locate(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/apply_locate.html")
