from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.models import CustomUser
from .models import Field, ConstructManager, EquipmentTypes, InstallLocate, DocsFile
from .forms import FieldForm


@login_required(login_url="/user/login/")
def index(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/main.html")


# 현장등록
@login_required(login_url="/user/login/")
def apply_field(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    form = FieldForm()
    equipments = EquipmentTypes.objects.all()
    return render(
        request,
        "system_manager/apply_field.html",
        {"form": form, "equipments": equipments},
    )


# 설치위치명 등록
@login_required(login_url="/user/login/")
def apply_locate(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/apply_locate.html")


# 문서 등록
@login_required(login_url="/user/login/")
def apply_document(request):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/apply_document.html")


@login_required(login_url="/user/login/")
def apply_document_template(request, type):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    files = DocsFile.objects.filter(type=type)
    return render(
        request,
        "system_manager/apply_document_template.html",
        {"type": type, "files": files},
    )


@login_required(login_url="/user/login/")
def upload_documents(request, type):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    files = request.FILES.getlist("file")
    for file in files:
        f = DocsFile(file=file, type=type, filename=file.name)
        f.save()
    return redirect("system_manager:apply_document_template", type=type)


@login_required(login_url="/user/login/")
def delete_documents(request, pk, type):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    DocsFile.objects.get(pk=pk).delete()
    return redirect("system_manager:apply_document_template", type=type)


# 사용자 등록 및 삭제
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
