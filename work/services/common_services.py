from user.models import CustomUser
import requests


def assign_user(user, doc, user_pk: int, link):
    target_user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "일반 관리자":
        doc.agentId = target_user
        doc.isCheckAgent = False
        doc.isCheckManager = True
        sms_send(link, [target_user.phone])
    elif user.class2 == "현장 대리인":
        doc.generalEngineerId = target_user
        doc.isCheckGeneralEngineer = False
        doc.isCheckAgent = True
        sms_send(link, [target_user.phone])
    elif user.class2 == "일반 건설사업관리기술인":
        doc.totalEngineerId = target_user
        doc.isCheckGeneralEngineer = True
        doc.isSuccess = False
        sms_send(link, [target_user.phone])
    else:
        doc.isSuccess = True
        doc.isCheckManager = False
        doc.isCheckAgent = False
        doc.isCheckGeneralEngineer = False
        sms_send(
            link,
            [
                doc.writerId.phone,
                doc.agentId.phone,
                doc.generalEngineerId.phone,
            ],
            1,
        )
    doc.save()
    return True


def sms_send(link, phone_list: list[str], sms_type: int = 0):
    send_url = "https://apis.aligo.in/send/"  # 요청을 던지는 URL, 현재는 문자보내기
    sender = "01025093834"  # 보내는 번호 => 현재 지영님 폰 번호만 인증이 되어서 다른 번호는 사용 불가

    phone_list = list(map(lambda x: x.replace("-", ""), phone_list))

    content = sms_content(link, sms_type)

    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

    sms_data = {
        "key": "axngr7ld8l3ng1qteoidm66axvjdlmdu",  # api key
        "userid": "jjy1229",  # 알리고 사이트 아이디
        "sender": sender,  # 발신번호
        "receiver": ",".join(phone_list),  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": content,  # 문자 내용
        "msg_type": "LMS",  # 메세지 타입 (SMS, LMS)
        "title": "[TQIMS 알림] TQIMS 결재 알림 안내",  # 메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
    }
    requests.post(send_url, data=sms_data)


def sms_content(link, sms_type: int = 0) -> str:
    return f"안녕하세요. 조립가설기자재 품질평가 및 관리시스템(TQIMS) 내 {'결재 요청' if sms_type == 0 else '검토 완료 알림'}이 도착하여 안내드립니다.\n\n결재 {'대기' if sms_type == 0 else '완료'} 문서 바로가기\n {link}"
