from django import forms
from django_summernote.widgets import SummernoteWidget

from . import models


class AnnouncePostForm(forms.ModelForm):
    class Meta:
        model = models.AnnouncePost
        fields = ["title", "content"]
        widgets = {
            "content": SummernoteWidget(),
        }
