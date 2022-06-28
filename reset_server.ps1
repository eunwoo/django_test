.venv/Scripts/Activate.ps1
Remove-Item "./db.sqlite3" -Force
python manage.py makemigrations
python manage.py migrate --run-sync
python manage.py loaddata ./init_data.yaml