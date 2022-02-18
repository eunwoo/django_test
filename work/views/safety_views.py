from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def safety(request):
    return render(request, "work/safety/safety.html")


@login_required(login_url="/user/login/")
def create_safety(request):
    return render(request, "work/safety/create_safety.html")


@login_required(login_url="/user/login/")
def update_safety(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_safety(request, pk):
    pass


@login_required(login_url="/user/login/")
def read_checklist(request, pk):
    pass
