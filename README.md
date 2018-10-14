# cookbox


# Setup

1) Install python 3.7, add it to path. (This may require builidng from source).
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

# Deployment to Apache on Debian

1) Install an Apache server: sudo apt-get install appache2; apt-get install appache2-dev;
3) Check that the installation was sucessful by connecting to localhost (or server ip), it should already serve a page saying that the installation worked. (To do so remotely you can do: ssh -L 9999:localhost:80 your_server; and then connect to localhost:9999.
9) Install Python3, not this does not have to be the latest Python version, check compatitability with Django version you're using: sudo apt-get install python3
9) Install pip: sudo apt-get install python3-pip;
3) Install all dependencies using pip as in *Setup*.
3) Install the WSGI  module for Apache: sudo apt-get install libapache2-mod-wsgi-py3
4) Check that mod_wsgi installation worked by staring a server: mod_wsgi-express start-server; This should start a server on localhost:8000.



## Documentation references
[mod_wsgi installation](https://pypi.org/project/mod_wsgi/)

# Switching databases
You can either use Sqlite or MySQL, the latter is prefered in production. To do edit the settings file comment out one of the items in the list called 'DATABASES'.

# Road map

1) REST Server
2) Web UI for the REST Server (This will be the MVP)
3) Native Android client
4) Native Windows client
5) More features ...
