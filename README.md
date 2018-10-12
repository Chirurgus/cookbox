# cookbox


# Setup

1) Install python 3.7, add it to path.
2) py -m pip install django
3) py -m pip install djangorestframework
4) py -m pip install django-nested-admin
5) py -m pip install Pillow
6) py -m pip install mysqlclient
1) Setup a database (Sqlite, or MySQL)
3) Describe how to connect to the above databse in settings.py
2) If necessairy add file with the databse password to file secrets/MYSQL_PASSWORD
7) py manage.py makemigrations
7) py manage.py migrate
8) py manage.py createsuperuser
9) Enter necesseary information
10) py manage.py runserver

# Switch between databases
You can either use Sqlite or MySQL, the latter is prefered in production. To do edit the settings file comment out one of the items in the list called 'DATABASES'.

# Road map

1) REST Server
2) Web UI for the REST Server (This will be the MVP)
3) Native Android client
4) Native Windows client
5) More features ...
