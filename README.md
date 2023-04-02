# BOARDIE BACKEND FOR BACKOFFICE

## How to run the project

- docker run --name my-postgres-db -e POSTGRES_PASSWORD=postgrespw -e POSTGRES_USER=postgres -e POSTGRES_DB=boardie-database -p 5432:5432 -d postgres:alpine3.17

- poetry install

- poetry shell

- alembic upgrade head

- uvicorn api.main:app --host 0.0.0.0

## How to check if the project is fine

- poetry shell

- poe check_all  (this is a custom command that runs many checkers)

## How to run everything with docker  

docker-compose up
