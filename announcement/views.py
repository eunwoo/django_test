from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import forms, models
from django.contrib import messages


@login_required(login_url="/user/login/")
def read_views(request, pk):
    item = get_object_or_404(models.AnnouncePost, pk=pk)
    return render(
        request,
        "announcement/read_announcement.html",
        {"item": item},
    )


@login_required(login_url="/user/login/")
def create_views(request):
    if request.method == "POST":
        form = forms.AnnouncePostForm(request.POST)
        if form.is_valid():
            announce = form.save(commit=False)
            announce.writer = request.user
            if "presave" in request.POST:
                announce.preSave = True
            announce.save()
            files = request.FILES.getlist("file_list")
            for file in files:
                announce.files.create(file=file)
            if announce.preSave == True:
                messages.success(request, "임시저장이 완료되었습니다.")
                return redirect("announcement:update_announcement", announce.pk)
            return redirect("announcement:announcement")
    else:
        pre_save_post = models.AnnouncePost.objects.filter(
            preSave=True, writer=request.user
        )
        if pre_save_post.count() > 0:
            messages.success(request, "임시저장한 문서를 불러왔습니다.")
            return redirect("announcement:update_announcement", pre_save_post[0].pk)
        form = forms.AnnouncePostForm()
    return render(
        request,
        "announcement/create_announcement.html",
        {"form": form},
    )


@login_required(login_url="/user/login/")
def update_views(request, pk):
    instance = get_object_or_404(models.AnnouncePost, pk=pk, writer=request.user)
    if request.method == "POST":
        form = forms.AnnouncePostForm(request.POST, instance=instance)
        if form.is_valid():
            announce = form.save(commit=False)
            announce.writer = request.user
            if "presave" in request.POST:
                announce.preSave = True
            else:
                announce.preSave = False
            announce.save()
            files = request.FILES.getlist("file_list")
            if files:
                announce.files.all().delete()
            for file in files:
                announce.files.create(file=file)
            if announce.preSave == True:
                messages.success(request, "임시저장이 완료되었습니다.")
                return redirect("announcement:update_announcement", announce.pk)
            return redirect("announcement:read_announcement", pk=pk)
    else:
        form = forms.AnnouncePostForm(instance=instance)
    return render(
        request,
        "announcement/create_announcement.html",
        {"form": form},
    )


@login_required(login_url="/user/login/")
def get_announcements(request):
    page = request.GET.get("page", 1)

    announcement_list = models.AnnouncePost.objects.all()

    paginator = Paginator(announcement_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "announcement/announcement.html",
        {"announcementitems": page_obj},
    )