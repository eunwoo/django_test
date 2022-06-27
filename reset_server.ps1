.venv/Scripts/Activate.ps1
Remove-Item "./db.sqlite3" -Force
python manage.py migrate
python manage.py loaddata ./init_data.json