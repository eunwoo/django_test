from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def quality_request(request):
    return render(request, "work/quality/quality_request/quality_request.html")


@login_required(login_url="/user/login/")
def create_quality_request(request):
    return render(request, "work/quality/quality_request/create_quality_request.html")


@login_required(login_url="/user/login/")
def update_quality_request(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_quality_request(request, pk):
    pass
