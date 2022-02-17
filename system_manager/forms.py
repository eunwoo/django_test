from django import forms

from .models import Field, ConstructManager


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = [
            "title",
            "callNum",
            "address",
            "orderer",
            "constructComp",
            "supervision",
            "startDay",
            "endDay",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "공사명을 입력해주세요."}
            ),
            "callNum": forms.TextInput(
                attrs={
                    "class": "col-12 text-center",
                    "placeholder": "현장 전화번호를 입력해주세요. ex) 010-1234-5678",
                    "pattern": "[0-9]{3}-[0-9]{4}-[0-9]{4}",
                }
            ),
            "address": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "현장 주소를 입력해주세요."}
            ),
            "orderer": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "발주자명을 입력해주세요."}
            ),
            "constructComp": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "종합건설업체명을 입력해주세요."}
            ),
            "supervision": forms.TextInput(
                attrs={
                    "class": "col-12 text-center",
                    "placeholder": "감리 및 CM 업체명을 입력해주세요.",
                }
            ),
            "startDay": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "col-12 text-center",
                    "placeholder": "착공일을 선택해주세요",
                    "type": "text",
                    "onfocus": "(this.type='date')",
                },
            ),
            "endDay": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "col-12 text-center",
                    "placeholder": "준공 예정일을 선택해주세요",
                    "type": "text",
                    "onfocus": "(this.type='date')",
                },
            ),
        }


class CmPhoneForm(forms.ModelForm):
    class Meta:
        model = ConstructManager
        fields = [
            "name",
            "belong",
            "phone",
        ]
