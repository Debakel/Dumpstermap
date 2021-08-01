# Dumpstermap Backend

## Getting Started
*Set up the development environment*

### Prerequisites
The application requires Python 3.6+ and a Postgres database with GIS extension.

### Setup
In order to start a basic docker container capable of serving a PostGIS-enabled database (with `postgres` as default user and database), run:

    docker run --name some-postgis -e POSTGRES_PASSWORD=mysecretpassword -d postgis/postgis
    
### Configuration
The application can be configured using a `.env` file. See [local.env.sample](local.env.sample) for all required and optional variables. 

If you use PyCharm, add the following to Django console's starting script:

    from dotenv import load_dotenv
    load_dotenv(verbose=True, dotenv_path='local.env')

## Heroku Deployment

Install Geo Buildpack (installs the Geo/GIS libraries used by GeoDjango):

    heroku buildpacks:add --index 1 https://github.com/heroku/heroku-geo-buildpack.git
    