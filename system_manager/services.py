import requests
import os


# 가입 승인 알림
def accept_send(phone):
    send_url = "https://apis.aligo.in/send/"  # 요청을 던지는 URL, 현재는 문자보내기
    sender = os.environ.get(
        "SENDER_NUMBER"
    )  # 보내는 번호 => 현재 지영님 폰 번호만 인증이 되어서 다른 번호는 사용 불가

    phone = phone.replace("-", "")  # - 제거

    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

    sms_data = {
        "key": "axngr7ld8l3ng1qteoidm66axvjdlmdu",  # api key
        "userid": "jjy1229",  # 알리고 사이트 아이디
        "sender": sender,  # 발신번호
        "receiver": phone,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": "조립 가설기자재 품질평가 및 관리 시스템 가입 승인이 완료되었습니다.",  # 문자 내용
        "msg_type": "SMS",  # 메세지 타입 (SMS, LMS)
        "title": "[T-QEM 알림] T-QEM 알림 안내",  # 메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
    }
    # requests.post(send_url, data=sms_data)
