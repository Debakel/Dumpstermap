# Dumpstermap Backend
Dumpstermap.org is a collaborative world wide map to share dumpster locations for others to find.

## Built with
### Backend
* Python, Django, Django REST framework (with [geospatial add-ons](https://github.com/openwisp/django-rest-framework-gis))
* PostgreSQL, PostGIS, Docker
* Deployed to Heroku

### Frontend
* TypeScript, Angular, Leaflet
* Deployed to Vercel

➡️ [Frontend Repository](https://github.com/Debakel/dumpstermap-ng)


## Screenshot

<img width="500" alt="grafik" src="https://user-images.githubusercontent.com/2857237/137350812-08b9ad62-106d-46f2-96d0-835f48481363.png">

## Development setup

### Prerequisites

The development setup requires Python 3.6, [pipenv](https://github.com/pypa/pipenv) and Docker to run a Postgres database with [GIS extension](https://postgis.net/).

To install the required python version and all dependencies, run:

    pipenv install

### Database

In order to start a basic docker container capable of serving a PostGIS-enabled database (with `postgres` as default
user and database), run:

     docker run -p 5432:5432 --name some-postgis -e POSTGRES_PASSWORD=mysecretpassword -d postgis/postgis

### Configuration

The application can be configured using environment variables or a `.env` file. See [local.env.sample](local.env.sample) for all required and
optional variables.

### Migrate database

Run `manage.py migrate` to create all database tables.

### Development server

Run `manage.py runserver` for a dev server.

### Running tests
Run `pipenv run pytest` to execute the unit tests.


## Deployment

Install Geo Buildpack (installs the Geo/GIS libraries used by GeoDjango):

    heroku buildpacks:add --index 1 https://github.com/heroku/heroku-geo-buildpack.git

 ## License
 tbd
