FROM postgres:10.6-alpine

ARG POSTGRES_DB_TEST
# Add creation of test db
RUN echo -e "CREATE DATABASE ${POSTGRES_DB_TEST};" > /docker-entrypoint-initdb.d/create.sql
