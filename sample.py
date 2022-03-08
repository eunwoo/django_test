import requests

send_url = "https://apis.aligo.in/send/"  # 요청을 던지는 URL, 현재는 문자보내기
sender = "01055555555"  # 보내는 번호

phone_list = map(lambda x: x.replace("-", ""), ["010-7176-7735"])

# ================================================================== 문자 보낼 때 필수 key값
# API key, userid, sender, receiver, msg
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

sms_data = {
    "key": "axngr7ld8l3ng1qteoidm66axvjdlmdu",  # api key
    "userid": "jjy1229",  # 알리고 사이트 아이디
    "sender": sender,  # 발신번호
    "receiver": ",".join(phone_list),  # 수신번호 (,활용하여 1000명까지 추가 가능)
    "msg": "샘플입니다.",  # 문자 내용
    "msg_type": "SMS",  # 메세지 타입 (SMS, LMS)
    # 'title' : 'title', #메세지 제목 (장문에 적용)
    # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
}
print(sms_data)
send_response = requests.post(send_url, data=sms_data)
print(send_response.json())
