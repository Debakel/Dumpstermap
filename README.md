# Dumpstermap Backend
[Dumpstermap.org](https://dumpstermap.org) is a collaborative world wide map to share dumpster locations for others to find.

## Built with
### Backend
* Python, Django, Django REST framework (with [geospatial add-ons](https://github.com/openwisp/django-rest-framework-gis))
* SQLite, SpatiaLite
* Deployed to [Fly.io](https://fly.io)

### Frontend
* TypeScript, Angular, Leaflet
* Deployed to Vercel

➡️ [Frontend Repository](https://github.com/Debakel/dumpstermap-ng)

## Development setup

### Prerequisites

The development setup requires:
* [uv](https://docs.astral.sh/uv/) (installs the required Python version automatically)
* [Geospatial libraries required by GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/geolibs/)
* [SpatiaLite](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/spatialite/)

To install the required python version and all python dependencies (including dev tools), run:

    uv sync --all-groups


### Configuration

The application can be configured using environment variables or a `.env` file. See [local.env.sample](local.env.sample) for all required and
optional variables.

### Migrate database

Run `make migrate` to create all database tables.

### Development server

Run `make test` for a dev server.

### Running tests
Run `make pytest` to execute the unit tests.

## Deployment

    fly deploy

## License
tbd
