from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..services.quality_request_services import create_quality_request_service


@login_required(login_url="/user/login/")
def quality_request(request):
    return render(request, "work/quality/quality_request/quality_request.html")


@login_required(login_url="/user/login/")
def create_quality_request(request):
    return create_quality_request_service(request)


@login_required(login_url="/user/login/")
def update_quality_request(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_quality_request(request, pk):
    pass


@login_required(login_url="/user/login/")
def require_sign_quality_request(request):
    pass
