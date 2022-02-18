from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def material(request):
    return render(request, "work/material/material.html")


@login_required(login_url="/user/login/")
def create_material(request):
    return render(request, "work/material/create_material.html")


@login_required(login_url="/user/login/")
def update_material(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_material(request, pk):
    pass
