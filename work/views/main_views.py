from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from work.services.main_services import get_unread_docs_list, get_unread_quality_docs


@login_required(login_url="/user/login/")
def index(request):
    context = get_unread_docs_list(request.user)
    return render(request, "work/main.html", context)


@login_required(login_url="/user/login/")
def quality_menu(request):
    context = get_unread_quality_docs(request.user)
    return render(request, "work/quality/menu.html", context)
