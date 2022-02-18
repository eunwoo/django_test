from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/user/login/")
def quality_report(request):
    return render(request, "work/quality/quality_report/quality_report.html")


@login_required(login_url="/user/login/")
def create_quality_report(request):
    return render(request, "work/quality/quality_report/create_quality_report.html")


@login_required(login_url="/user/login/")
def update_quality_report(request, pk):
    pass


@login_required(login_url="/user/login/")
def delete_quality_report(request, pk):
    pass
