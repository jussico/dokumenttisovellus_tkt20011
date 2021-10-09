#!/bin/bash

# set -x
set -e

komento="psql -v ON_ERROR_STOP=1"

echo "$komento < prelude/schema.sql"
$komento < prelude/schema.sql

echo "$komento < scripts/test_data.sql"
$komento < scripts/test_data.sql

echo "@done. database state set with test data."

echo "database now:"

$komento < scripts/query_database.sql
