# Django_inha

인하대학교 건설 프로젝트

# 초기설치

- python manage.py makemigrations
- python manage.py migrate --run-syncdb
- python manage.py loaddata init_data.yaml

# 작업 관리

- 모든 페이지의 작성 페이지는 일반 관리자만 가능
- 모든 페이지의 수정 페이지는 관리자마다 다르게 적용
- 모든 페이지의 읽기 모드는 모든 관리자가 해당되도록

# 장고 쿼리셋

https://gaussian37.github.io/python-django-django-query-set/

# 모델 초기 데이터

https://runebook.dev/ko/docs/django/howto/initial-data

# 폼 리스트 형식으로 받아오기

https://kgu0724.tistory.com/105

- 해당 기능은 Django의 기능이 아닌 javascript, html로 구현하자

# 장고 알람 메세지

https://devlog.jwgo.kr/2020/10/17/fancy-messaging-system-in-django/

# HTML to PDF

https://blog.naver.com/rnjsrldnd123/221526274628

# 포맷터 설정하기

https://nuggy875.tistory.com/110

# 수동 폼 작성

https://wikidocs.net/70855

# 페이지네이터

https://wikidocs.net/71240

# Django Ajax

https://initstory.tistory.com/20

# 서명 시 이미지 넣기

https://pbj0812.tistory.com/240

# JS 로 Form 관리

https://stackoverflow.com/questions/50774176/sending-file-and-json-in-post-multipart-form-data-request-with-axios

# 마지막 모델 불러오기 (문서 번호 작성시 사용)

https://stackoverflow.com/questions/1256190/django-getting-last-object-created-simultaneous-filters

# choice 필드 사용하기

https://ssungkang.tistory.com/entry/Django-ChoiceField-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

# Form 작업 이전에 확인

https://ssungkang.tistory.com/entry/Django-ChoiceField-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

# Django Model 만든날짜, 수정된날짜 자동 추가

https://stackoverflow.com/questions/3429878/automatic-creation-date-for-django-model-form-objects

# PDF 이어서 붙이기

https://medium.com/nerd-for-tech/dynamically-create-and-merge-pdfs-in-angular-using-jspdf-and-pdf-lib-aa82ae35f1e3

# 수정해야 할 사항

- ~가입시 이미지 전송이 안됨 => 이전에는 되는 것처럼 보이게만 짜둠~ => 해결완료
- ~문서번호를 제목에 띄우는건 힘듦, 대신 작성후 000-1번 문서로 저장되었습니다 같은 알림메세지는 가능~ => 성공함

# 넘긴 사항

- 설치 위치 등록 페이지
- 페이지네이트 작성하기 (위 링크 참고)
- 투입 공종 직접입력 란 (https://close-up.tistory.com/entry/Select-%EB%B0%95%EC%8A%A4-%EC%84%A0%ED%83%9D%EA%B0%92-input%EC%97%90-%EB%84%A3%EA%B8%B0-ex-email-%EC%A3%BC%EC%86%8C%EC%84%A0%ED%83%9D)
- 결과 보고 시 강관비계, 시스템비계, 시스템 동바리 선택창 => 문서 작성시 해당 속성이 입력되어야 하는데 없음

# 참고사항

- User의 Register 속성을 True로 하면 사용권한을 획득한다.

# 02/15 해야할 것

- 사용자는 각 이용자당 한명씩이다 (현장 대리인 한 명, 일반관리자 한 명 등등)
- 해당 사항을 고려하여 디비설계

# 02/15 마무리

- navbar_sys.html, apply_field.html 작성중 중단
- 계획보다 많이 제작

# 02/16 해야할 것

- 시스템 관리자 페이지 작성

# 02/16 마무리

- 시스템 관리자 사용자 등록 삭제 완료
- 문서 등록, 구조 계산서와 시공상세도면 미완성
- 현장 등록, 설치위치명 등록은 미완성

# 02/17 해야할 것

- 업무 페이지 및 구조 안전성 검토 패키지
- 문서 등록 마무리
- 현장 등록 및 설치 위치명 등록

# 02/17 마무리

- 품질검사 의뢰서 모델 작성 중 중단
- 일단 디비 전부 설정해두기

# 02/18 해야할 것

- 디비 전부 설정
- 체크리스트 목록 작성
- 기존 코드 연결하기

# 02/18 마무리

- 설치 작업 페이지를 제외하고 html 연동
- 모델 전부 작성
- javascript or jquery를 통한 form을 작성해야함
- 요청 views 만들기 => 역할마다 disable 할 것은 기존 코드가 조금 되어있음

# 02/21 마무리

- 유저 사인 전송
- 유저 삭제 오류 수정
- 구조 안전성 검토 신고서 작성 중 중단

# 02/22 해야할 것

- 구조 안전성 검토 신고서 작성서 완료하기
- 구조 안전성 검토 신고서 목록 페이지 제작하기

# 02/22 마무리

- 구조 안전성 검토 신고서 60프로 완성
- 파일 불러오고 전송하는 작업을 진행해야함
- 유저별로 권한을 다르게 부여하도록 진행

# 02/23 해야할 것

- 구조 안전성 검토 파일 업로드 작성
- 구조 안전성 검토 서명 요청 과정 작성
- (추가) 구조 안전성 검토 목록 페이지 작성

# 02/24 해야할 것

- 구조 안전성 검토 전체 루트 제작
- 협업을 위한 코드 리펙토링
- 구조 안전성 검토 읽기 전용 페이지 제작
- (추가) 구조 안전성 검토 체크리스트 페이지 제작
- (추가) 이메일 연동 작업

# 02/25 해야 할 것

- 구조 안전성 검토 총괄 관리자 페이지 설정
- 배포 (오후 2시까지)

# 개발 사항

- 시스템 관리자 메뉴 설치위치명 등록 제외 전부 동작
- 구조 안전성 검토 신고서 루트 개발 완료(일반 관리자, 현장 대리인, 일반 건설사업기술관리인, 총괄 건설사업기술관리인)
- 테스트시 각 계정별로 아이디를 하나씩 만든후 테스트 하시면 됩니다.
  - 시스템 관리자, 일반 관리자, 현장 대리인, 일반 건설사업기술관리인, 총괄 건설사업관리기술인 총 5명 입니다.
  - 현재 이메일연동은 하지 않은 상태입니다.
- 그 외 자재 반입, 품질검사 의뢰, 품질검사 성과보고, 설치작업 확인 페이지는 구조 안전성 검토 신고서 문서를 기반으로 재활용하여 개발할 예정입니다.

# 할일 정리

- 문서 갯수 표시
- 시스템 관리자 설치위치명 등록
- 자재 공급원 신고서
  - 공급원 등록이 좀 시간이 걸릴듯
  - 붙임 부분에서 내용을 업로드하는게 어려울듯
- 품질검사 의뢰서 작성
  - 시료 채취 장소를 업로드 하는 부분이 어려울 듯
- 품질검사 성과 보고 작성
- 설치작업 전 체크리스트 작성
- 설치작업 중 체크리스트 작성

# 02/25 마무리

- 자재 공급원 신고서 작성 => 서명과 공급원 연결하기
- 자재 공급원 신고서 기타사항은 크게 하고, 읽기 전용일때는 체크박스로 넣기
- 3/4 까지 마무리할 계획 세우기

# 참고자료

https://getbootstrap.com/docs/5.1/forms/input-group/

# 품질검사 의뢰서

- 시료 채취 장소는 일단 패스하기
- 보내야 할것은 품질검사 의뢰서 폼, 현장 등록에 추가된 현장

# 02/28 마무리

- 품질검사 의뢰서 일반 관리자 부분 작성
- 디비 초기화 후 다시 실행하기

# 해야할 일 정리

- 품질검사 의뢰서 - 현장대리인, 일반 건설사업기술인
- 품질검사 총괄 신고서 - 일반관리자, 현장대리인, 일반 건설사업기술인, 총괄 건설사업기술인
- 설치작업 전 페이지 - 일반관리자
- 설치작업 후 페이지 - 일반관리자
- 설치장소 등록 - 시스템 관리자
- 결과보고 페이지 - 전체 공통

# Todo

- 개발 안될거 같은거 정리하기

# 03/03 남은 작업

- 품질검사 성과표 서명 요청 (현장대리인, 일반 건설사업관리기술인, 총괄 건설사업관리기술인)
- 설치위치 등록 (시스템 관리자)
- 설치작업 체크리스트 등록 (일반 관리자)
- 결과보고 페이지 (전체 관리자)
- 업무에서 안읽은 문서 태그 넣기

# 03/03 마무리

- 설치 위치 등록에서 구분1, 2, 3 추가하는것 완료
- 구분3에서 체크박스 한것을 등록하는걸 추가해야함
- InstallLocate 모델에서 boolean 필드를 추가함 => 동기화는 아직 안시킴


# 03/04 마무리

- https://www.codehim.com/text-input/jquery-multiple-image-upload-with-preview-and-delete/
- 위 링크는 이미지 업로드 방법
- 설치작업 전 체크리스트 작성도중 중단
- 해당 작업은 create와 update 탬플릿을 따로 관리할 예정


# 3월 2주차 남은 작업

- 설치작업 전 페이지
- 설치작업 중 페이지
- 결과보고 페이지
- 기타 남은 작업
  - 저장 시 팝업이 아닌 알림처럼

# 03/07 해야할 일

- 설치작업 전 업데이트 탬플릿 만들기
- 설치작업 전 읽기 전용 페이지 제작하기
- 설치작업 중 탬플릿 제작하기
- 설치작업 중 읽기 전용 페이지 제작하기

# 해야할 일

- 설치작업전 체크리스트 리드 문서

# 03/08 작업 리스트

- 오전: 설치작업 전 체크리스트 마무리하기
- 오후: 설치작업 중 체크리스트 작성하기

# 03/08 마무리
- 품질검사 성과보고부터 내용 수정하기
- 문자 전송 서비스를 주석 처리함, 사용할 경우 주석을 제거하기


# 사용시 해야 할 일
- 문자메세지 API 서버 IP 등록하기


# 결과보고 정리
- 강관비계 시스템비계 시스템 동바리 등 종류 체크시 어떻게 분류?
- 설치위치는 어떻게 분류?

# 해야할 일
- 품질검사 성과총괄표 전부 => 완료
- 구조 안전성 검토 - 직접입력 만들기 => 완료


# 03/10 작업 마무리
- create material 만 작업후 종료
- 결과보고 페이지 작성중 종료 => annotate를 이용하여 문서 불러오기
- 문자 전송기능 끄고 작업하기


# 금 계획
- 작업 마무리 짓기
- 설치작업 확인 체크 시 종류 및 설치위치가 추가됨

# 상세 계획
- 오전 : 결과보고 페이지 작성하기 => 해당 문서 클릭시 read 페이지로 읽기
- 오후 : 오전 작업을 이어서, 수정사항 반영하기, 주간 보고서 작성하기

# 웹에디터
- https://blog.devgenius.io/best-free-wysiwyg-editor-python-django-admin-panel-integration-d9cb30da1dba
- https://bookpark.github.io/2018-02-01/django-ckeditor

# 아이디, 비밀번호 찾기 구현

- DB 에 인증번호 저장, 만료 시간을 설정하기
- DB에 저장할 목록 : 인증번호, IP Address, 만료시간
- IP Address 받기 : https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django

# 04/12
- 미흡시 내용입력 확인하기
- 수정 시 점검항목 입력부분 추가
- 설치작업중 체크리스트 수정하기

# 04/12 마무리
- 위 작업 전부 완료
- 구조안전성 검토 체크리스트는 디자인 전부 수정되어야 함
- 아이디 비밀번호찾기 -> 디자인 받은 후 수정. DB와 문자를 이옹한 방법이 될듯함