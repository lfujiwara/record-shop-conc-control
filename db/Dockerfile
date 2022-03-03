FROM postgres:14-alpine

COPY ./migrations/*up.sql /docker-entrypoint-initdb.d
COPY ./seed/ /docker-entrypoint-initdb.d/
