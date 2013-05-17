# Commands to vaccum, analyze and backup itwishlist_postgresql_db - add to crontab
/usr/bin/sudo -u postgres /usr/bin/pg_dump -Fc itwishlist_postgresql_db > /opt/backups/prevac.gz
/usr/bin/sudo -u postgres /usr/bin/vacuumdb --analyze itwishlist_postgresql_db
/usr/bin/sudo -u postgres /usr/bin/pg_dump -Fc itwishlist_postgresql_db > /opt/backups/postvac.gz
SCHEMA_BACKUP="/opt/backups/$(date +%w).db.schema"
sudo -u postgres /usr/bin/pg_dump -C -s itwishlist_postgresql_db > $SCHEMA_BACKUP