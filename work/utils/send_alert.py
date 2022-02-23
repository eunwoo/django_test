from user.models import CustomUser


def email_send(user_pk: int):
    email = CustomUser.objects.get(pk=user_pk).email
    # 이메일 전송 함수 만들기
    print(f"이메일은 다음과 같습니다. {email}")
    # ==========================================================
    return email
