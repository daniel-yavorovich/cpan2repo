= Description =

cpan2repo - free software for automated build debian packages from the repository with git-perl-code.

Builder can also read and collect cpanfile debian packages required dependencies cpan.

cpan2repo - developed within company Adcamp and Pult Group

= Installation =

== Create MySQL database and user ==

After create please change DATABASES settings in settings.py

mysql> create database cpan2repo character set utf8;
mysql> grant all on cpan2repo.* to 'cpan2repo'@'localhost' identified by 'secret';
mysql> flush privileges;

== Create RabbitMQ user and virtual host ==

After create please change BROKER_URL settings in settings.py

# rabbitmqctl add_user cpan2repo secret
# rabbitmqctl add_vhost cpan2repo
# rabbitmqctl set_permissions -p cpan2repo cpan2repo ".*" ".*" ".*"

== Deploy cpan2repo ==

# useradd -s /bin/bash -m -g users agent
# cd /home/agent
# cp bin/check_core_module.pl /usr/local/bin/check_core_module.pl
# git clone https://github.com/daniel-yavorovich/cpan2repo.git
# pip install -r cpan2repo/requirements.txt
# su - agent
$ cd cpan2repo
$ tee cpan2repo/local_settings.py << EOF
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'cpan2repo',
       'USER': 'cpan2repo',
       'PASSWORD': 'secret',
       'HOST': '',
       'PORT': ''
    }
}

BROKER_URL = 'amqp://cpan2repo:secret@localhost:5672/cpan2repo
EOF
$ python manage.py syncdb --all
$ python manage.py migrate --fake
$ exit

# apt-get -y install gunicorn
# tee /etc/gunicorn.d/cpan2repo << EOF
CONFIG = {
    'mode': 'wsgi',
    'working_dir': '/home/agent/cpan2repo',
    'user': 'www-data',
    'group': 'www-data',
    'args': (
        '--bind=127.0.0.1:8081',
        '--workers=4',
        'cpan2repo.wsgi',
    ),
}
EOF
# service gunicorn restart

# nginx=stable # use nginx=development for latest development version
# add-apt-repository ppa:nginx/$nginx
# apt-get update
# apt-get install nginx
# tee /etc/nginx/sites-available/cpan2repo << EOF
server {
        listen 80 default_server;
        server_name cpan2repo.example.com;

        location / {
                proxy_pass http://127.0.0.1:8081;
                proxy_redirect http://127.0.0.1:8081 http://cpan2repo.example.com;
        }

        location /static/ {
                root /usr/local/lib/python2.7/dist-packages/django/contrib/admin;
        }
}
EOF
# rm -f /etc/nginx/sites-enabled/default
# ln -snf /etc/nginx/sites-available/cpan2repo /etc/nginx/sites-enabled/cpan2repo
# nginx -s reload

# apt-get -t install supervisor
# service supervisord stop
# tee /etc/supervisor/conf.d/cpan2repo.conf << EOF
[program:celeryd]
user=root
group=root
environment=C_FORCE_ROOT="yes"
directory=/home/agent/cpan2repo
command=/usr/bin/python /home/agent/cpan2repo/manage.py celeryd
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/celeryd.log
stdout_logfile=/var/log/supervisor/celeryd.log

[program:celerybeat]
user=root
group=root
environment=C_FORCE_ROOT="yes"
directory=/home/agent/cpan2repo
command=/usr/bin/python /home/agent/cpan2repo/manage.py celerybeat
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/celerybeat.log
stdout_logfile=/var/log/supervisor/celerybeat.log
EOF
# service supervisord start

## Create directory per branch. For example: cron job for branch "base" and "staging"
# mkdir -p /var/lib/repo/dists/base/main/binary-amd64 /var/lib/repo/dists/staging/main/binary-amd64
# ln -s /var/lib/repo/dists/base/main/binary-amd64 /var/lib/repo/dists/base/main/binary-i386
# ln -s /var/lib/repo/dists/staging/main/binary-amd64 /var/lib/repo/dists/staging/main/binary-i386

# tee /etc/cron.d/rebuild_repo << EOF
# Job per branch. For example: cron job for branch "staging"
* * * * *       root    /usr/local/bin/rebuild_repo.sh staging 2>&1 | logger -t debarchiver -p daemon.info
# Job for build default branch for cpan requirements:
* * * * *       root    mv /home/agent/cpan2repo/build/*.deb /var/lib/repo/dists/base/main/binary-amd64/; /usr/local/bin/rebuild_repo.sh base 2>&1 | logger -t debarchiver -p daemon.info
EOF

== External auth ==

=== Redmine auth settings ===

AUTHENTICATION_BACKENDS  = (
        'django.contrib.auth.backends.ModelBackend',
        'redmineauth.backends.Redmine',
)

REDMINE_URL = 'https://redmine.example.com'

=== Jira auth settings ===

AUTHENTICATION_BACKENDS = (
    'webui.backends.JiraBackend',
    'django.contrib.auth.backends.ModelBackend',
)

JIRA_URL = "https://jira.example.com/jira/rest"

= License =

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.