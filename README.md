# Trashmap
## Requirements  
* postgres with postgis
* pip install shapely geojson configparser flask sqlalchemy psycopg2
* apt-get install postgresql postgis python-pip python2.7 postgresql-server-dev-all python-psycopg2
* apt-get install postgis*

## Installation
* enable postgis in postgres by running `sudo -u postgres psql -d trashmap -c "CREATE EXTENSION postgis;"`

### Setup notes
* apt-get install language-pack-de-base (bei locales fehler während postgresql installation)

## Deploy to webserver
### Apache
* apt-get install apache2 libapache2-mod-wsgi
* create deploy.py with `from Trashmap import app as application`
### Tornado
* `./run_tornado.py`
* 
#### nginx as proxy  

Here’s a simple nginx configuration which proxies to an application served on localhost at port 8000, setting appropriate headers:
```
  server {
    listen 80;

    server_name dumpstermap.mrtz.me;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:8000/;
        proxy_redirect     off;

        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    }
}
```
