from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import forms, models
from django.contrib import messages


# 법률정보 조회
@login_required(login_url="/user/login/")
def read_views(request, pk):
    item = get_object_or_404(models.LawPost, pk=pk)
    return render(
        request,
        "law/read_law.html",
        {"item": item},
    )


# 법률정보 작성
@login_required(login_url="/user/login/")
def create_views(request):
    if request.method == "POST":
        form = forms.LawPostForm(request.POST)
        if form.is_valid():
            law = form.save(commit=False)
            law.writer = request.user
            if "presave" in request.POST:
                law.preSave = True
            law.save()
            files = request.FILES.getlist("file_list")
            for file in files:
                law.files.create(file=file)
            if law.preSave == True:
                messages.success(request, "임시저장이 완료되었습니다.")
                return redirect("law:update_law", law.pk)
            return redirect("law:law")
    else:
        pre_save_post = models.LawPost.objects.filter(preSave=True, writer=request.user)
        if pre_save_post.count() > 0:
            messages.success(request, "임시저장한 문서를 불러왔습니다.")
            return redirect("law:update_law", pre_save_post[0].pk)
        form = forms.LawPostForm()
    return render(
        request,
        "law/create_law.html",
        {"form": form},
    )


# 법률정보 수정
@login_required(login_url="/user/login/")
def update_views(request, pk):
    instance = get_object_or_404(models.LawPost, pk=pk, writer=request.user)
    if request.method == "POST":
        form = forms.LawPostForm(request.POST, instance=instance)
        if form.is_valid():
            law = form.save(commit=False)
            law.writer = request.user
            if "presave" in request.POST:
                law.preSave = True
            else:
                law.preSave = False
            law.save()
            files = request.FILES.getlist("file_list")
            if files:
                law.files.all().delete()
            for file in files:
                law.files.create(file=file)
            if law.preSave == True:
                messages.success(request, "임시저장이 완료되었습니다.")
                return redirect("law:update_law", law.pk)
            return redirect("law:read_law", pk=pk)
    else:
        form = forms.LawPostForm(instance=instance)
    return render(
        request,
        "law/create_law.html",
        {"form": form},
    )


# 법률정보 목록
@login_required(login_url="/user/login/")
def get_laws(request):
    page = request.GET.get("page", 1)

    law_list = models.LawPost.objects.filter(preSave=False).order_by("-created_on")

    paginator = Paginator(law_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "law/law.html",
        {"lawitems": page_obj},
    )


# 법률정보 삭제
@login_required(login_url="/user/login/")
def delete_laws(request):
    if request.method == "POST":
        law_list = request.POST.getlist("law_list[]")
        models.LawPost.objects.filter(pk__in=law_list).delete()
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "fail"}, status=400)
