import random
from datetime import timedelta
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from user.models import ChangePwd, CustomUser
from user.services import code_send

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
        return render(request, "auth/editAdmin.html", {"form": form})
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
        return render(request, "auth/editUser.html", {"form": form})


def id_check(request):
    if request.method == "POST":
        username = request.POST["username"]
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"result": "deny"})
        else:
            return JsonResponse({"result": "success"})
    return Http404()


def find_menu(request):
    return render(request, "auth/find/menu.html")


def find_id(request):
    if request.method == "POST":
        name = request.POST["name"]
        call = request.POST["call"]
        user = CustomUser.objects.filter(name=name, phone=call)
        if user:
            return JsonResponse({"result": "success", "id": user[0].username})
        else:
            return JsonResponse({"result": "deny"})
    return render(request, "auth/find/id.html")


def require_code(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        phone = request.POST["call"]
        user = CustomUser.objects.filter(username=id, name=name, phone=phone)
        if not user:
            return JsonResponse({"result": "deny"})
        else:
            user = user[0]
        code = f"{random.randrange(1, 10**6):06}"
        ChangePwd.objects.create(user=user, code=code)
        code_send(code, phone)
        return JsonResponse({"result": "success"})
    return Http404()


def reset_pwd(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        phone = request.POST["call"]
        user = CustomUser.objects.filter(username=id, name=name, phone=phone)
        if not user:
            return JsonResponse({"result": "deny"})
        else:
            user = user[0]
        code = request.POST["code"]
        request_log = ChangePwd.objects.filter(user=user, code=code)
        if not request_log:
            return JsonResponse({"result": "deny"})
        else:
            request_log = request_log[0]
        expired_time = request_log.expired_time + timedelta(minutes=5)
        if expired_time < timezone.now():
            return JsonResponse({"result": "deny"})
        request_log.isSuccess = True
        return render(
            request,
            "auth/find/reset_pwd.html",
            {
                "userId": user.username,
                "code": code,
            },
        )
    return render(request, "auth/find/password.html")


def reset_pwd_success(request):
    if request.method == "POST":
        code = request.POST["code"]
        username = request.POST["userId"]
        new_password = request.POST["password"]
        user = CustomUser.objects.get(username=username)
        request_log = ChangePwd.objects.filter(
            user=user,
            code=code,
            isSuccess=True,
        )
        if not request_log:
            return JsonResponse({"result": "deny"})
        else:
            request_log[0].delete()
        user.set_password(new_password)
        user.save()
        return JsonResponse({"result": "success"})
    return Http404()
