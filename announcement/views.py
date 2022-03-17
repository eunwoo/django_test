from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import forms, models


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
            announce.save()
            files = request.FILES.getlist("file_list")
            for file in files:
                announce.files.create(file=file)
            return redirect("announcement:announcement")
    else:
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
            announce.save()
            files = request.FILES.getlist("file_list")
            if files:
                announce.files.all().delete()
            for file in files:
                announce.files.create(file=file)
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
