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

The default development setups (`dev.env`) uses SQLite as the database
backend. Meaning that the database will be lost when the container shuts down.

## fail2ban

The following setup is used with fail2ban.

# /etc/fail2ban/filter.d/cookbox-apache.conf
[Definition]
failregex = ^<HOST> - - \[.*\] "(GET|POST|HEAD) /(wp-admin|wp-login|admin|phpmyadmin|phpMyAdmin|mysql|sql|\.php|\.asp|\.jsp|actuator|api/|\.env|\.git|\.svn|backup|config|db|database|test|tmp|temp|upload|uploads|shell|cmd|eval|exec|system|proc|passwd|shadow|etc/passwd|\.well-known/security\.txt|sitemap\.xml|robots\.txt|crossdomain\.xml|clientaccesspolicy\.xml|\.htaccess|\.htpasswd|web\.config|index\.php\?s=|think\w)" HTTP/[0-9]\.[0-9]" (400|404|403|500) .*$
            ^<HOST> - - \[.*\] "(GET|POST|HEAD) .*(union|select|insert|drop|delete|update|script|javascript|vbscript|onload|onerror|alert|document\.cookie|eval\(|base64_decode|exec\(|system\(|passthru\(|shell_exec\(|file_get_contents\(|curl_exec\(|fopen\(|fwrite\(|include\(|require\().*" HTTP/[0-9]\.[0-9]" .*$
            ^<HOST> - - \[.*\] ".*" [45]\d\d \d+ ".*" ".*(bot|crawler|spider|scraper|scanner|nikto|nmap|sqlmap|dirb|gobuster|wfuzz|hydra|masscan|nessus|openvas|acunetix|burp|zap).*"$

# /etc/fail2ban/filter.d/cookbox-auth.log

[Definition]
# Match failed login attempts from your Django log format
failregex = ^WARNING .* Failed login attempt - User: .*, IP: <HOST>, User Agent: .*$

# Optional: Match successful logins to reset ban counter (uncomment if desired)
# ignoreregex = ^INFO .* Successful login - User: .*, IP: <HOST>, User Agent: .*$

# Date pattern to match your log timestamp format
datepattern = ^%%Y-%%m-%%d %%H:%%M:%%S,%%f

# /etc/fail2ban/jail.local
[cookbox-auth]
enabled = true
port = http,https
filter = cookbox-auth
logpath = /home/pi/cookbox/logs/auth_attempts.log
maxretry = 5
findtime = 600
bantime = 3600
action = iptables-multiport[name=cookbox-auth, port="http,https", protocol=tcp]

[cookbox-apache]
enabled = true
filter = cookbox-apache
logpath = /home/pi/cookbox/logs/access.log
port = http,https
maxretry = 5
findtime = 600
bantime = 3600
action = iptables-multiport[name=cookbox-apache, port="http,https", protocol=tcp]


