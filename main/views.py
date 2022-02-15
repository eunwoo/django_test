from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/user/login/")
def home(request):
    user = request.user
    return render(request, "main/home.html", {"user": user})
