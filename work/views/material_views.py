from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..services.material_services import create_material_service


@login_required(login_url="/user/login/")
def material(request):
    return render(request, "work/material/material.html")


@login_required(login_url="/user/login/")
def create_material(request):
    return create_material_service(request)


@login_required(login_url="/user/login/")
def update_material(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_material(request, pk):
    pass
