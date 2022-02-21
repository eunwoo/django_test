from django.shortcuts import render, redirect

from . import forms
from .utils import decodeDesignImage


def usertype(request):
    return render(request, "auth/usertype.html")


def agreeForUser(request):
    return render(request, "auth/agreeForUser.html")


def registerUser(request):
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)  # commit False시 DB에 저장하지 않음
            image_file = decodeDesignImage(
                request.POST["signImage"], form.instance.username
            )
            answer.signImage = image_file
            answer.save()
            return redirect("user:login")
    else:
        form = forms.UserForm()
    return render(request, "auth/registerUser.html", {"form": form})


def agreeForAdmin(request):
    return render(request, "auth/agreeForAdmin.html")


def registerAdmin(request):
    if request.method == "POST":
        form = forms.AdminForm(request.POST)
        if form.is_valid():
            form.instance.register = True
            form.instance.is_system_manager = True
            form.save()
            return redirect("user:login")
    else:
        form = forms.AdminForm()
    return render(request, "auth/registerAdmin.html", {"form": form})
