from django import forms

from ..models import MaterialSupplyReport


class GeneralManagerMaterialSupplyReportForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplyReport
        fields = [
            "date",
            "title",
            "constructType",
            "text",
            "businessLicense",
            "deliveryPerformanceCertificate",
            "safetyCertificate",
            "qualityTestReport",
            "testPerformanceComparisonTable",
        ]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control text-wrap", "rows": 3, "cols": 50}
            ),
            "businessLicense": forms.FileInput(attrs={"class": "form-control"}),
            "deliveryPerformanceCertificate": forms.FileInput(
                attrs={"class": "form-control"}
            ),
            "safetyCertificate": forms.FileInput(attrs={"class": "form-control"}),
            "qualityTestReport": forms.FileInput(attrs={"class": "form-control"}),
            "testPerformanceComparisonTable": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }


class GeneralEngineerMaterialSupplyReportForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplyReport
        fields = ["replyDate", "generalEngineerText", "result"]
