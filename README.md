# 처음 사용자 가이드

- 해당문서는 개발과 유지보수를 위해 만들어졌습니다.
- 데이터베이스 구조는 [여기](https://www.erdcloud.com/d/Ltkr3eeGtRk37g9sx)를 참고하시면 됩니다.
- 작업 진행 상황은 Git 또는 work_log.md 를 참고해주세요.

# 폴더 구조

- announcement : 공지사항
- inha : 프로젝트 세팅
- law : 법령정보
- result : 결과보고
- system_manager : 기본정보 등록
- user : 로그인/회원가입 관련
- work : 업무
  - safety : 구조 안전성 검토
  - material : 자재 반입
  - quality_request : 품질검사 의뢰
  - quality_report : 품질검사 성과보고
  - before_install : 설치작업 전 체크리스트
  - install : 설치작업 중 체크리스트


# 초기 작업
- [Poetry를 설치해 주세요.](https://python-poetry.org/docs/#installation)
- [Poetry를 설정해 주세요.](https://amazingguni.medium.com/python-poetry%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%A5%BC-vscode%EC%97%90%EC%84%9C-%EA%B0%9C%EB%B0%9C%ED%95%A0-%EB%95%8C-interpreter%EB%A5%BC-%EC%9E%A1%EB%8A%94-%EB%B0%A9%EB%B2%95-e1806f093e6d)
- .env 파일을 설정해주세요.
- 아래 내용을 전부 명령어로 입력하세요.
  - poetry install & poetry update              관련 패키지 설치
  - python manage.py makemigrations             데이터베이스 구조 설정
  - python manage.py migrate --run-syncdb       데이터베이스 제작
  - python manage.py loaddata init_data.yaml    초기 데이터 추가 (체크리스트 질문 목록 등)

# 실행
- python manage.py runserver                    서버 실행

# 초기화
- db.sqlite3를 지우시고 Poetry 설치를 제외한 초기 작업을 전부 실행해주세요.