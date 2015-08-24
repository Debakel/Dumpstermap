# Trashmap
## Requirements  
* postgres with postgis
* psycopg2
* pip install shapely geojson configparser flask sqlalchemy psycopg2
* apt-get install postgresql postgis python-pip python2.7 postgresql-server-dev-all python-psycopg2
* apt-get install postgis*
## Installation
* enable postgis in postgres by running `sudo -u postgres psql -d trashmap -c "CREATE EXTENSION postgis;"`

### Setup notes
* apt-get install language-pack-de-base

## Deploy to webserver
### Apache
* apt-get install apache2 libapache2-mod-wsgi
* create deploy.py with `from Trashmap import app as application`