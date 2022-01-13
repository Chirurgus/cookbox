# cookbox

Cookbox is a personal recipe database, made accessible via a website.

## Updating production server

1. Pull the desired release, from the production branch for example: `git pull origin production`
1. Enter the python virtual environment: `source cookbox.venv/bin/activate`
1. Update/install required python libraries: `pip3 install -r requirements.txt`
1. Migrate the database: `python3 manage.py migrate`
1. Collect static files: `python3 manage.py collectstatic;`
1. Check if the app is functional: `python3 manage.py check`
1. Run tests: `python3 manage.py test`
1. Restart Apache2: `sudo service apache2 restart`


## Setup for developpment

1. Install python 3.7, add it to path.
1. `python3 pip3 install -r requirements.txt`
1. `py manage.py makemigrations`
1. `py manage.py migrate`
1. `py manage.py createsuperuser`
1. Enter necessary information
1. `py manage.py runserver`


## Using docker

Setup using docker is easy, just run: `docker-compse build`,
and run with `docker-compose up -d`.

You will, however, need to set multiple environment variables. `dev.env` has
some defaults suitable for a development environment (not suitable at all of 
any sort of production environment). The easiest way to use these variables
is to create a copy and rename it to `.env`.

The images are based on `arm32v7/debian` which is likely
not what you want, unless you're running them on a Raspberry Pi.
The same goes for the `mariadb` image used.

The default development setups (`dev.env`) uses SQLite as the database
backend. Meaning that the database will be lost when the container shuts down.
If using Docker, prefer using `mariadb` by setting `DB_ENGINE=mysql` in
`.env`.


# Loading mysql dumps

First start the mysql container with `sudo docker-compose up -d db`,
then load the dump with `mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -P3305 -h0.0.0.0 ${MYSQL_DATABSE} < dump.sql`

