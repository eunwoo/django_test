from django import forms

from ..models import InstallCheckList


class InstallCheckListForm(forms.ModelForm):
    class Meta:
        model = InstallCheckList
        fields = [
            "date",
            "detailLocate",
        ]
