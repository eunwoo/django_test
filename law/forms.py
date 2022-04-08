from django import forms
from django_summernote.widgets import SummernoteWidget

from . import models


class LawPostForm(forms.ModelForm):
    class Meta:
        model = models.LawPost
        fields = ["title", "content"]
        widgets = {
            "content": SummernoteWidget(),
        }
