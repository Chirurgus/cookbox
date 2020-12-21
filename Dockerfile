FROM debian:10.7

RUN mkdir /opt/cookbox/
WORKDIR /opt/cookbox
COPY . /opt/cookbox/

RUN apt-get update && \
	apt-get -y --no-install-recommends install \
		python3 python3-pip python3-dev git sqlite apache2 apache2-utils \
		libapache2-mod-wsgi-py3 mariadb-client build-essential \
		default-libmysqlclient-dev

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

# Setup Apache
RUN cat apache2.conf >> /etc/apache2/apache2.conf
RUN a2enmod wsgi

RUN mkdir /opt/cookbox/logs

CMD python3 manage.py check && \
	python3 manage.py collectstatic --noinput && \
	python3 manage.py migrate && \
	apachectl -D FOREGROUND
