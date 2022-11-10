FROM arm32v7/debian:10.7-slim

RUN mkdir /opt/cookbox/
WORKDIR /opt/cookbox

RUN chown root:www-data /opt/cookbox

COPY --chown=root:www-data cookbox /opt/cookbox/cookbox
COPY --chown=root:www-data cookbox_admin /opt/cookbox/cookbox_admin
COPY --chown=root:www-data cookbox_core /opt/cookbox/cookbox_core
COPY --chown=root:www-data cookbox_glossary /opt/cookbox/cookbox_glossary
COPY --chown=root:www-data cookbox_recipeui /opt/cookbox/cookbox_recipeui
COPY --chown=root:www-data cookbox_scraper /opt/cookbox/cookbox_scraper
COPY --chown=root:www-data cookbox_seasons /opt/cookbox/cookbox_seasons
COPY --chown=root:www-data cookbox_webui /opt/cookbox/cookbox_webui
COPY --chown=root:www-data manage.py requirements.txt apache2.conf /opt/cookbox/

RUN apt-get update && \
	apt-get -y --no-install-recommends install \
		python3 python3-pip python3-dev git sqlite apache2 apache2-utils \
		libapache2-mod-wsgi-py3 mariadb-client build-essential \
		default-libmysqlclient-dev python3-lxml libjpeg-dev zlib1g-dev

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

# Setup Apache
RUN cat apache2.conf >> /etc/apache2/apache2.conf
RUN a2enmod wsgi
RUN a2dissite 000-default default-ssl
RUN mkdir /opt/cookbox/logs

CMD python3 manage.py check && \
	python3 manage.py collectstatic --noinput && \
	python3 manage.py migrate && \
	sed -i "s/__SERVER_NAME__/$SERVER_NAME/g" /etc/apache2/apache2.conf && \
	sed -i "s/__SERVER_ALIAS__/$SERVER_ALIAS/g" /etc/apache2/apache2.conf && \
	sed -i "s/__SERVER_ADMIN_EMAIL__/$SERVER_ADMIN_EMAIL/g" /etc/apache2/apache2.conf && \
	apachectl -D FOREGROUND
