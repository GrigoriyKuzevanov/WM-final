# Team manager

## Installation
Clone this repo and get into it:
```shell
git clone https://github.com/GrigoriyKuzevanov/WM-final.git && cd WM-final
```

Use Poetry to create virtual environment and install dependencies:
```shell
poetry install
```



## Configuration

Into the project directory create an `.env-compose` file for running database with docker compose:

```shell
touch .env-compose
```

Add the following variables with values to the `.env-compose` file:

```env
# main-db
DB_USER=wm-user
DB_PASSWORD=wm-password
DB_NAME=wm-db-name

# redis
REDIS_PASSWORD=redis-password
REDIS_USER=redis-user
REDIS_USER_PASSWORD=redis-user-password
```

Into the app directory create `.env` file with application configuration:

```shell
touch ./app/.env
```

Add the following variables with values to the `.env file:

```env
# Run application
CONFIG__RUN__APP=main:app
CONFIG__RUN__HOST=localhost
CONFIG__RUN__PORT=8000
CONFIG__RUN__AUTO_RELOAD=True

# Main database
CONFIG__MAIN_DB__DB_USER=wm-user
CONFIG__MAIN_DB__DB_PASSWORD=wm-password
CONFIG__MAIN_DB__DB_HOST=localhost
CONFIG__MAIN_DB__DB_PORT=5431
CONFIG__MAIN_DB__DB_NAME=wm-db-name

# Redis
CONFIG__REDIS__USER=redis-user
CONFIG__REDIS__PASSWORD=redis-user-password
CONFIG__REDIS__HOST=localhost
CONFIG__REDIS__PORT=6380
CONFIG__REDIS__DB=0

# Fastapi-users
# access token secrets
CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET=<your secret>
CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET=<your secret>

# superuser credentials
CONFIG__SUPERUSER__EMAIL=<your admin email>
CONFIG__SUPERUSER__PASSWORD=<your admin password>
CONFIG__SUPERUSER__NAME=<your admin name>
CONFIG__SUPERUSER__LAST_NAME=<your admin last name>
CONFIG__SUPERUSER__INFO=<your admin info>

# Starlette-admin
# session middleware
CONFIG__SESSION_MIDDLEWARE__SECRET_KEY=<your secret>
```
To generate secrets, use the following command:

```shell
python -c "import secrets; print(secrets.token_hex())"
```

## Running

Run docker compose:

```shell
docker compose --env-file .env-compose  up -d
```

Run the application:

```shell
uvicorn app.main:app --reload
```


## Usage

### Superuser
Before using the application you need to create the first superuser:

```shell
python -m app.scripts.create_superuser
```

Use the credentials you provided in `.env` file to log in.

### Admin

Admin interface uses [starlette-admin](https://jowilf.github.io/starlette-admin/) and is available by default at `localhost:8000/admin`

### API documentation
API endpoints and documentation are available by default at `localhost:8000/docs`
