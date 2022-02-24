from django import forms

from ..models import SafetyReport


class GeneralManagerSafetyReportForm(forms.ModelForm):
    class Meta:
        model = SafetyReport
        fields = ["docNum", "date", "title", "constructType", "text"]


class GeneralEngineerSafetyReportForm(forms.ModelForm):
    class Meta:
        model = SafetyReport
        fields = ["replyDate", "generalEngineerText", "result"]
