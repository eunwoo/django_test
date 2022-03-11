from django import forms

from ..models import QualityPerformanceReport


class GeneralManagerQualityPerformanceReportForm(forms.ModelForm):
    class Meta:
        model = QualityPerformanceReport
        fields = ["date"]
