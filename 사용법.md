# 가상환경 추가
- poetry install & poetry update

# 디비 생성
- python manage.py makemigrations
- python manage.py migrate --run-syncdb
- python manage.py loaddata init_data.yaml

# 실행
- python manage.py runserver