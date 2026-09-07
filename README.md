# Dumpstermap Backend
[Dumpstermap.org](https://dumpstermap.org) is a collaborative world wide map to share dumpster locations for others to find.

## Built with
### Backend
* Python, Django, Django REST framework (with [geospatial add-ons](https://github.com/openwisp/django-rest-framework-gis))
* PostgreSQL, PostGIS, Docker
* Deployed to Heroku

### Frontend
* TypeScript, Angular, Leaflet
* Deployed to Vercel

➡️ [Frontend Repository](https://github.com/Debakel/dumpstermap-ng)

## Development setup

### Prerequisites

The development setup requires:
* [uv](https://docs.astral.sh/uv/) (installs the required Python version automatically)
* [Geospatial libraries required by GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/geolibs/)
* Docker to run a Postgres database with [GIS extension](https://postgis.net/).

To install the required python version and all python dependencies (including dev tools), run:

    uv sync --all-groups

### Database

In order to start a basic docker container capable of serving a PostGIS-enabled database (with `postgres` as default
user and database), run:

     docker run -p 5432:5432 --name some-postgis -e POSTGRES_PASSWORD=mysecretpassword -d postgis/postgis

### Configuration

The application can be configured using environment variables or a `.env` file. See [local.env.sample](local.env.sample) for all required and
optional variables.

### Migrate database

Run `uv run manage.py migrate` to create all database tables.

### Development server

Run `uv run manage.py runserver` for a dev server.

### Running tests
Run `uv run pytest` to execute the unit tests.


## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

 ## License
 tbd
