#!/bin/bash

set -x

################################################################
# postgresql 8.4.4
# http://wiki.postgresql.org/wiki/YUM_Installation
/usr/pgsql-9.1/bin/initdb -U postgres -D /var/lib/pgsql/9.1/data
systemctl enable postgresql-9.1.service
systemctl start postgresql-9.1.service
/usr/pgsql-9.1/bin/createdb -U postgres retail
/usr/pgsql-9.1/bin/psql -U postgres -c "create user retail with password 'retail';"
/usr/pgsql-9.1/bin/psql -U postgres -c "alter database retail owner to retail;"
