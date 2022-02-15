from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def index(request):
    if not request.user.is_system_manager: # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/main.html")


# 현장등록
def apply_field(request):
    if not request.user.is_system_manager: # 시스템 매니저만 접근 가능
        return redirect("main:home")
    pass


# 설치위치명 등록
def apply_locate(request):
    if not request.user.is_system_manager: # 시스템 매니저만 접근 가능
        return redirect("main:home")
    pass


# 문서 등록
def apply_document(request):
    if not request.user.is_system_manager: # 시스템 매니저만 접근 가능
        return redirect("main:home")
    pass


# 사용자 등록 및 삭제
def user_management(request):
    if not request.user.is_system_manager: # 시스템 매니저만 접근 가능
        return redirect("main:home")
    pass
