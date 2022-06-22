from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# 메인화면
@login_required(login_url="/user/login/")
def home(request):
    user = request.user
    return render(request, "main/home.html", {"user": user})
