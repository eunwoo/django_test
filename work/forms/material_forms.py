from django import forms

from ..models import MaterialSupplyReport


class GeneralManagerMaterialSupplyReportForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplyReport
        fields = [
            "date",
            "constructType",
            "text",
        ]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control text-wrap", "rows": 3, "cols": 50}
            )
        }


class GeneralEngineerMaterialSupplyReportForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplyReport
        fields = ["replyDate", "generalEngineerText", "result"]


class TotalEngineerMaterialSupplyReportForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplyReport
        fields = ["totalEngineerText", "result"]
