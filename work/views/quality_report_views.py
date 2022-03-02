from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..services.quality_report_services import (
    create_quality_report_service,
    update_quality_report_service,
)


@login_required(login_url="/user/login/")
def quality_report(request):
    return render(request, "work/quality/quality_report/quality_report.html")


@login_required(login_url="/user/login/")
def create_quality_report(request):
    return create_quality_report_service(request)


@login_required(login_url="/user/login/")
def update_quality_report(request, pk):
    return update_quality_report_service(request, pk)


@login_required(login_url="/user/login/")
def delete_quality_report(request, pk):
    pass


@login_required(login_url="/user/login/")
def require_sign_quality_report(request, pk):
    pass
