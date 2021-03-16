Initialize venv (once):
```bash
python -m venv venv
```

Activate venv:
MacOS/Linux: . venv/bin/activate
Windows (cmd): venv\Scripts\activate
Windows (bash): source venv/Scripts/activate

Django installation:
```bash
pip install django
```

Start Django Server (from backend):
```bash
cd backend
python manage.py runserver
```

(Once) Create Super User
```bash
python manage.py createsuperuser
```


1- (Once by app) Créer l'application
```bash
mkdir apps/organization
python manage.py startapp 
```

2- Ajouter l'application au fichier project/settings.py
3- Register le model dans admin.py

4- Update Database Schema
```bash
python manage.py makemigrations
python manage.py migrate
```