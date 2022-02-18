from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def index(request):
    return render(request, "work/main.html")


@login_required(login_url="/user/login/")
def quality_menu(request):
    return render(request, "work/quality/menu.html")
