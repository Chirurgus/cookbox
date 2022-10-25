# cookbox

Cookbox is a personal recipe database, made accessible via a website.

## Updating production server

1) Pull the desired release, from the production branch for example: `git pull origin production`
1) Enter the python virtual envirement: `source cookbox.venv/bin/activate`
1) Update/install required python libraries: `pip3 install -r requirements.txt`
1) Migrate the database: `python3 manage.py migrate`
1) Collect static files: `python3 manage.py collectstatic;`
1) Check if the app is functional: `python3 manage.py check`
1) Run tests: `python3 manage.py test`
1) Restart Apache2: `sudo service apache2 restart`

## Setup for developpment

1) Install python 3.7, add it to path.
2) `python3 pip3 install -r requirements.txt`
7) `py manage.py makemigrations`
7)` py manage.py migrate`
8) `py manage.py createsuperuser`
9) Enter necessary information
10) `py manage.py runserver`

# Saving/loading mysql dumps

First start the mysql container with `sudo docker-compose up -d db`.
Then you can save and load the database dump with the following commands :

```
# Load enviroment variables from `.env` configuration
export     $(grep MYSQL_USER .env)
export $(grep MYSQL_PASSWORD .env)
export $(grep MYSQL_DATABASE .env)
sudo docker-compose exec db bash -c 'mysqldump -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}' > database.sql 2 >> error.log
sudo docker exec -i cookbox_db_1 bash -c 'mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}' < database.sql
```

