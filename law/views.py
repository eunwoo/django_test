from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import forms, models


@login_required(login_url="/user/login/")
def read_views(request, pk):
    item = get_object_or_404(models.LawPost, pk=pk)
    return render(
        request,
        "law/read_law.html",
        {"item": item},
    )


@login_required(login_url="/user/login/")
def create_views(request):
    if request.method == "POST":
        form = forms.LawPostForm(request.POST)
        if form.is_valid():
            law = form.save(commit=False)
            law.writer = request.user
            law.save()
            files = request.FILES.getlist("file_list")
            for file in files:
                law.files.create(file=file)
            return redirect("law:law")
    else:
        form = forms.LawPostForm()
    return render(
        request,
        "law/create_law.html",
        {"form": form},
    )


@login_required(login_url="/user/login/")
def update_views(request, pk):
    instance = get_object_or_404(models.LawPost, pk=pk, writer=request.user)
    if request.method == "POST":
        form = forms.LawPostForm(request.POST, instance=instance)
        if form.is_valid():
            law = form.save(commit=False)
            law.writer = request.user
            law.save()
            files = request.FILES.getlist("file_list")
            if files:
                law.files.all().delete()
            for file in files:
                law.files.create(file=file)
            return redirect("law:read_law", pk=pk)
    else:
        form = forms.LawPostForm(instance=instance)
    return render(
        request,
        "law/create_law.html",
        {"form": form},
    )


@login_required(login_url="/user/login/")
def get_laws(request):
    page = request.GET.get("page", 1)

    law_list = models.LawPost.objects.all()

    paginator = Paginator(law_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "law/law.html",
        {"lawitems": page_obj},
    )
