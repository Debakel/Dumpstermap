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

## Development
**Prerequisites:** [Docker](https://www.docker.com/) and [make](https://www.gnu.org/software/make/)


- `make test` to run unit tests
- `make runserver` to start a dev server on [localhost:8000](http://localhost:8000)
- `make migrate` to apply database migrations


## Deployment

    fly deploy

## License
tbd
