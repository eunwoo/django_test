from django import forms

from ..models import BeforeInstallCheckList


class BeforeInstallCheckListForm(forms.ModelForm):
    class Meta:
        model = BeforeInstallCheckList
        fields = [
            "date",
            "detailLocate",
            "title",
        ]
