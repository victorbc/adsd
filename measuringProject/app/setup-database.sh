#!/bin/sh

set -ex

mysql -u root -e 'DROP DATABASE IF EXISTS adsd'
mysql -u root -e 'CREATE DATABASE adsd'

python -c 'import todo; todo.db.create_all()'
