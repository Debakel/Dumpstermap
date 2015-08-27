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

## Deployment
### Tornado (with nginx)
Tornado is an open source version of the scalable, non-blocking web server and tools that power FriendFeed. Because it is non-blocking and uses epoll, it can handle thousands of simultaneous standing connections, which means it is ideal for real-time web services. Integrating this service with Flask is straightforward (run_tornado.py):  
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
