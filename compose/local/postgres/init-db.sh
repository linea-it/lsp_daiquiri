#!/bin/bash
set -e
# GRANT CREATE ON DATABASE daiquiri_data TO $POSTGRES_USER;

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE daiquiri_app WITH OWNER $POSTGRES_USER;
    CREATE DATABASE daiquiri_data WITH OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE daiquiri_data TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "daiquiri_data" <<-EOSQL
    CREATE SCHEMA tap_schema AUTHORIZATION $POSTGRES_USER;
    CREATE SCHEMA tap_upload AUTHORIZATION $POSTGRES_USER;
    CREATE SCHEMA oai_schema AUTHORIZATION $POSTGRES_USER;
EOSQL

# Create Table DR2 SAMPLE SCHEMA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "daiquiri_data" <<-EOSQL
    \i /data/des_dr2_sample.sql;
EOSQL
# -- CREATE INDEX coadd_objects_ra_dec ON des_dr2.main USING btree (q3c_ang2ipix(ra, "dec"));

# Create Table GAIA SAMPLE SCHEMA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "daiquiri_data" <<-EOSQL
    \i /data/gaia_dr3_sample.sql;
EOSQL

# Create Table TWOMASS SAMPLE SCHEMA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "daiquiri_data" <<-EOSQL
    \i /data/twomass_sample.sql;
EOSQL
