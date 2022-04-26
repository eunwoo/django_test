from user.models import CustomUser
import requests


def assign_user(user, doc, user_pk: int, link):
    target_user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "일반 사용자":
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
        "title": "[T-QEM 알림] T-QEM 알림 안내",  # 메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
    }
    requests.post(send_url, data=sms_data)


def sms_content(link, sms_type: int = 0) -> str:
    context = ""
    link_text = ""
    if sms_type == 0:
        context = "결재 요청"
        link_text = "결재 대기 문서"
    elif sms_type == 1:
        context = "검토 완료 알림"
        link_text = "결재 완료 문서"
    elif sms_type == 2:
        context = "설치작업 전 점검 조치사항 알림"
        link_text = "조치사항 항목"
    elif sms_type == 3:
        context = "설치작업 중 점검 조치사항 알림"
        link_text = "조치사항 항목"
    return f"안녕하세요. 조립가설기자재 품질평가 및 관리시스템(T-QEM) 내 {context}이 도착하여 안내드립니다.\n\n{link_text} 바로가기\n {link}"


def image_send(message_list, user_phone):
    send_url = "https://apis.aligo.in/send/"  # 요청을 던지는 URL, 현재는 문자보내기
    sender = "01025093834"  # 보내는 번호 => 현재 지영님 폰 번호만 인증이 되어서 다른 번호는 사용 불가

    for data in message_list:
        sms_data = {
            "key": "axngr7ld8l3ng1qteoidm66axvjdlmdu",  # api key
            "userid": "jjy1229",  # 알리고 사이트 아이디
            "sender": sender,  # 발신번호
            "receiver": user_phone.replace("-", ""),  # 수신번호 (,활용하여 1000명까지 추가 가능)
            "msg": data["content"],  # 문자 내용
            "msg_type": "LMS",  # 메세지 타입 (SMS, LMS)
            "title": "[T-QEM 알림] T-QEM 알림 안내",  # 메세지 제목 (장문에 적용)
            # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
        }

        # 이미지 입력, 절대경로, 상대경로 상관없음.
        for image in list(data["img"]):
            files = {"image": image.file}
            send_response = requests.post(send_url, data=sms_data, files=files)
            print(send_response.json())
