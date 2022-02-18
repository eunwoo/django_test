# Django_inha

인하대학교 건설 프로젝트

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

# 수정해야 할 사항

- 가입시 이미지 전송이 안됨 => 이전에는 되는 것처럼 보이게만 짜둠
- 시스템관리자는 한명만 가입하도록
- 문서번호를 제목에 띄우는건 힘듦, 대신 작성후 000-1번 문서로 저장되었습니다 같은 알림메세지는 가능

# 넘긴 사항

- 설치 위치 등록 페이지
- 페이지네이트 작성하기 (위 링크 참고)

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

- 품질검사 의뢰서 작성 중 중단
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