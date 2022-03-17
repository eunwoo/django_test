from django import forms
from django_summernote.widgets import SummernoteWidget


class SomeForm(forms.Form):
    foo = forms.CharField(widget=SummernoteWidget())
