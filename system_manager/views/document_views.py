from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..models import DocsFile


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


# 구조 계산서, 시공상세도면 페이지
@login_required(login_url="/user/login/")
def detail_menu(request, type):
    if not request.user.is_system_manager:  # 시스템 매니저만 접근 가능
        return redirect("main:home")
    return render(request, "system_manager/detail_menu.html", {"type": type})
