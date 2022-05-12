from django import forms

from ..models import QualityInspectionRequest


class GeneralManagerQualityInspectionRequestForm(forms.ModelForm):
    class Meta:
        model = QualityInspectionRequest
        fields = [
            "goods",
            "title",
            "size",
            "sampleQuentity",
            "sampleOrigin",
            "testType_hweem",
            "testType_zip",
            "testType_tensile",
            "sampleDate",
            "testStandard",
            "isImportFacility",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "제목을 입력해주세요."}
            ),
            "size": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "규격을 입력해주세요. (여러 개 입력 가능)",
                }
            ),
            "sampleQuentity": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "시료량을 입력해주세요. (여러 개 입력 가능)",
                }
            ),
            "sampleOrigin": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "생산국을 입력해주세요."}
            ),
            "testType_hweem": forms.CheckboxInput(),
            "testType_zip": forms.CheckboxInput(),
            "testType_tensile": forms.CheckboxInput(),
        }
        labels = {
            "testType_hweem": "휨하중",
            "testType_zip": "압축하중",
            "testType_tensile": "인장하중",
        }


class AgentQualityInspectionRequestForm(forms.ModelForm):
    class Meta:
        model = QualityInspectionRequest
        fields = ["orderDate"]
