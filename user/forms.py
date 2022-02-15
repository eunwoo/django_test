from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class AdminForm(UserCreationForm):
  
      email = forms.EmailField(label="이메일",
          widget=forms.TextInput(
              attrs={"class": "col-12 text-center", "placeholder": "이메일을 입력해주세요"}
          ))
      
      username = forms.CharField(
          required=True,
          widget=forms.TextInput(
              attrs={"class": "col-12 text-center", "placeholder": "아이디를 입력해주세요"}
          ),
      )

      password1 = forms.CharField(
          required=True,
          widget=forms.PasswordInput(
              attrs={"class": "col-12 text-center", "placeholder": "비밀번호를 입력해 주세요"}
          ),
      )

      password2 = forms.CharField(
          required=True,
          widget=forms.PasswordInput(
              attrs={"class": "col-12 text-center", "placeholder": "비밀번호를 입력해 주세요"}
          ),
      )
      
      class Meta:
        model = CustomUser
        fields = (
            "username",
            "name",
            "email",
            "phone",
            "signImage",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "이름을 입력해주세요"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "전화번호를 입력해주세요."}
            ),
        }


class UserForm(AdminForm):
    class Meta:
        affiliation_choices = [
            ("--------------", "-----------"),
            ("종합건설업체", "종합건설업체"),
            ("감리 및 CM 업체", "감리 및 CM 업체"),
        ]

        roletype_choices = [
            ("--------------", "-----------"),
            ("일반 관리자", "일반 관리자"),
            ("현장 대리인", "현장 대리인"),
            ("시스템 관리자", "시스템 관리자"),
            ("일반 건설사업관리기술인", "일반 건설사업관리기술인"),
            ("총괄 건설사업관리기술인", "총괄 건설사업관리기술인"),
        ]

        role_choices = [
            ("--------------", "-----------"),
            ("시공 관리자", "시공 관리자"),
            ("품질 관리자", "품질 관리자"),
            ("안전 관리자", "안전 관리자"),
            ("해당 사항 없음", "해당 사항 없음"),
        ]
        model = CustomUser
        fields = (
            "username",
            "name",
            "email",
            "class1",
            "class2",
            "class3",
            "phone",
            "signImage",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "이름을 입력해주세요"}
            ),
            "class1": forms.Select(
                attrs={"class": "col-12 text-center"}, choices=affiliation_choices
            ),
            "class2": forms.Select(
                attrs={"class": "col-12 text-center"}, choices=roletype_choices
            ),
            "class3": forms.Select(
                attrs={"class": "col-12 text-center"}, choices=role_choices
            ),
            "phone": forms.TextInput(
                attrs={"class": "col-12 text-center", "placeholder": "전화번호를 입력해주세요."}
            ),
        }