# Trashmap

## Setup
### Install Requirements
Requirements:
* Python 2.7 (with  shapely geojson configparser flask sqlalchemy psycopg2 geoalchemy2)
* Postgres Database (with PostGIS extension)

Install all requirements by running:
```
$ apt-get install postgresql postgis python-pip python2.7 postgresql-server-dev-all python-psycopg2
$ apt-get install postgis*
$ pip install shapely geojson configparser flask sqlalchemy psycopg2 geoalchemy2 tornado
```

### Create Database
On most systems you need to be authenticated as the PostgreSQL super user (usually named postgres) in order to execute many of the commands below.
The following will create a new database user called `bob`, a new database called `trashmap` and enables the postgis extension for the new database:

```
$ sudo -u postgres createuser -P bob
$ sudo -u postgres createdb --encoding=UTF8 --owner=bob trashmap
$ sudo -u postgres psql -d trashmap -c "CREATE EXTENSION postgis;"
```

### Start application
Start the (dev) server by running `python trashmap/Trashmap.py`.

## Deployment
### Tornado (with nginx)
Tornado is an open source version of the scalable, non-blocking web server and tools that power FriendFeed. Because it is non-blocking and uses epoll, it can handle thousands of simultaneous standing connections, which means it is ideal for real-time web services.
Integrating this service with Flask is straightforward (`run_tornado.py`):
```
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from trashmap.Trashmap import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()
```

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

## Notes
* npm install --save-dev grunt-wiredep (To inject Bower packages into your source code with Grunt.)
* apt-get install language-pack-de-base (bei locales fehler während postgresql installation)
