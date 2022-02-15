from django.shortcuts import render, redirect

from . import forms


def usertype(request):
    return render(request, "auth/usertype.html")


def agreeForUser(request):
    return render(request, "auth/agreeForUser.html")


def registerUser(request):
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = forms.UserForm()
    return render(request, "auth/registerUser.html", {"form": form})


def agreeForAdmin(request):
    return render(request, "auth/agreeForAdmin.html")


def registerAdmin(request):
    if request.method == "POST":
        form = forms.AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = forms.AdminForm()
    return render(request, "auth/registerAdmin.html", {"form": form})
