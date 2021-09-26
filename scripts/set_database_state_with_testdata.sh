#!/bin/bash

# set -x
set -e

echo "psql < prelude/schema.sql"
psql < prelude/schema.sql

echo "psql < scripts/test_data.sql"
psql < scripts/test_data.sql

echo "@done. database state set with test data."

echo "database now:"

psql < scripts/query_database.sql
