from django import forms
from django.forms import ModelForm, widgets

from .models import SafetyReport


class SafetyForm(forms.ModelForm):
    class Meta:
        conType_choices = [
            ("----", "----"),
            ("건축", "건축"),
            ("토목", "토목"),
            ("기계", "기계"),
            ("직접", "직접"),
        ]
        model = SafetyReport
        fields = (
            "docNum",
            "date",
            "title",
            "conType",
            "content",
            "inCharge",
            "gcSiteAgent",
            "doc",
            "replyDate",
            "inChargeRevCom",
            "managerRevCom",
            "results",
            "eng",
            "gcEng",
        )
        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "날짜를 선택해주세요",
                    "type": "date",
                },
            ),
            "title": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "제목을 입력해주세요"}
            ),
            "conType": forms.Select(
                attrs={"class": "col-12 text-center", "placeholder": "투입 공종을 선택해주세요"},
                choices=conType_choices,
            ),
            "content": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "내용을 입력해주세요"}
            ),
            "inCharge": forms.TextInput(attrs={"class": "col-12"}),
            "gcSiteAgent": forms.TextInput(attrs={"class": "col-12"}),
            "doc": forms.FileInput(attrs={"class": "col-12"}),
            "replyDate": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "col-12",
                    "placeholder": "날짜를 선택해주세요",
                    "type": "text",
                    "onfocus": "(this.type='date')",
                },
            ),
            "inChargeRevCom": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "내용을 입력해 주세요"}
            ),
            "managerRevCom": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "내용을 입력해 주세요"}
            ),
            "results": forms.TextInput(
                attrs={"class": "col-12", "placeholder": "결과를 선택해 주세요"}
            ),
            "eng": forms.TextInput(attrs={"class": "col-12"}),
            "gcEng": forms.TextInput(attrs={"class": "col-12"}),
        }
