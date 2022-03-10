from django.shortcuts import render, redirect

from . import forms
from .utils import decodeDesignImage
from django.contrib import messages


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
            messages.success(request, "가입이 완료되었습니다.")
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
            sys_manager = form.save(commit=False)
            sys_manager.class1 = "종합건설업체"
            sys_manager.class2 = "시스템 관리자"
            image_file = decodeDesignImage(
                request.POST["signImage"], form.instance.username
            )
            sys_manager.signImage = image_file
            sys_manager.save()
            messages.success(request, "가입이 완료되었습니다.")
            return redirect("user:login")
    else:
        form = forms.AdminForm()
    return render(request, "auth/registerAdmin.html", {"form": form})


def editUser(request):
    user = request.user
    if user.is_system_manager:
        if request.method == "POST":
            form = forms.AdminForm(request.POST, instance=user)
            if form.is_valid():
                answer = form.save(commit=False)  # commit False시 DB에 저장하지 않음
                image_file = decodeDesignImage(
                    request.POST["signImage"], form.instance.username
                )
                if image_file:
                    answer.signImage = image_file
                answer.save()
                return redirect("main:home")
        else:
            form = forms.AdminForm(instance=user)
        return render(request, "auth/registerAdmin.html", {"form": form})
    else:
        if request.method == "POST":
            form = forms.UserForm(request.POST, instance=user)
            if form.is_valid():
                answer = form.save(commit=False)  # commit False시 DB에 저장하지 않음
                image_file = decodeDesignImage(
                    request.POST["signImage"], form.instance.username
                )
                if image_file:
                    answer.signImage = image_file
                answer.save()
                return redirect("main:home")
        else:
            form = forms.UserForm(instance=user)
        return render(request, "auth/registerUser.html", {"form": form})
