#!/bin/sh

set -ex

# createDBs
mysql -u root -p -e 'DROP DATABASE IF EXISTS adsd'
mysql -u root -p -e 'CREATE DATABASE adsd'

python -c 'import measurement; measurement.db.create_all()'
