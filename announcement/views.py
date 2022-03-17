from django.shortcuts import render

from . import forms

# Create your views here.
def create_views(request):
    form = forms.SomeForm()
    return render(
        request,
        "announcement/create_announcement.html",
        {"form": form},
    )
