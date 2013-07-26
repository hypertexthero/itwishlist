# IT Wishlist Docs

## Software Stack

The deployed stack for <http://it.ippc.int> consists of the following components installed in our QA & TEST server **exlqaippc2.ext.fao.org
- 193.43.36.204**:

- [NGINX](http://nginx.org/en/) - public facing web server - serves media and proxies dynamic requests to Gunicorn
- [Gunicorn](http://gunicorn.org/ "Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.") - internal HTTP application server
- [PostgreSQL](http://www.postgresql.org/docs/) - database server
- [Django](http://djangoproject.com/) web application in Git repository at `/opt/projects/itwishlist-env/itwishlist`. The master repository is at <https://github.com/hypertexthero/itwishlist/>.

## Restarting it.ippc.int Server {#restart}

Note that we will eventually have a [Fabric](http://docs.fabfile.org/en/1.6/) script that will do all of the below with one command. =TODO: Set up Fabric deployment script.

1. Login to exlqaippc2.ext.fao.org (193.43.36.204) via SSH:

        ssh root@exlqaippc2.ext.fao.org

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd /opt/projects/itwishlist-env && . bin/activate && cd itwishlist

3. Find out the number of the Gunicorn process:

        ps aux | grep gunicorn

4. Kill the process (replace #### with the number from the output above):

        kill -HUP ####

5. Restart the Gunicorn server:

        gunicorn --daemon wsgi:application

You shouldn't need to restart Nginx as well, but in case you do:

## Working on it.ippc.int Code

1. Fork the project code at the main repository <https://github.com/hypertexthero/itwishlist>
2. [Use the Github flow approach to create a new branch to add features you want](http://scottchacon.com/2011/08/31/github-flow.html), and work on it in your local machine. When ready, commit changes to your fork and [send a pull request](https://help.github.com/articles/using-pull-requests) to get it pushed into production. When you're a bit more comfortable with the system you will gain direct commit access to the main repository.
3. =TODO: Documentation on getting started with Django, including installing local requirements.

## Deploying Code to it.ippc.int Server

1. Login to exlqaippc2.ext.fao.org (193.43.36.204) via SSH:

        ssh root@exlqaippc2.ext.fao.org

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd /opt/projects/itwishlist-env && . bin/activate && cd itwishlist

3. Pull changes from the Github repository master branch:

        git pull origin master

4. Collect static files to static directories in case you changed CSS, JavaScript, site design images, etc (say 'yes' when it asks to overwrite):

        python manage.py collectstatic

5. If you changed Python code, you need to <a href="#restarting-itippcint-server">restart</a> the server, too. If you only changed code in templates, there is no need to restart. =TODO: Setup [South](http://south.aeracode.org/) and add migration instructions in case we are changing data models.

## Reverting to Previous Commit in Case You Break Something

1. Login to exlqaippc2.ext.fao.org (193.43.36.204) via SSH:

        ssh root@exlqaippc2.ext.fao.org

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd /opt/projects/itwishlist-env && . bin/activate && cd itwishlist

3. [Find the hash of the previous commit in your repository](http://git-scm.com/book/en/Git-Basics-Viewing-the-Commit-History):

        git log

4. Checkout previous commit from [the Github repository master branch](https://github.com/hypertexthero/itwishlist/commits/master) using [these instructions](http://stackoverflow.com/a/4114122/412329) or the command below:

         git reset --hard HashOfPreviousCommitHereLotsOfNumberAndLetters

5. [Restart it.ippc.int server](#restart)

## Backing Up it.ippc.int Postgres Database

1. Login to exlqaippc2.ext.fao.org (193.43.36.204) via SSH:

        ssh root@exlqaippc2.ext.fao.org

2. Run the following commands one after the other. Backups are stored in `/opt/backups/` =TODO: setup automatic backup script and add to crontab:

        # Commands to vaccum, analyze and backup itwishlist_postgresql_db - add to crontab
        /usr/bin/sudo -u postgres /usr/bin/pg_dump -Fc itwishlist_postgresql_db > /opt/backups/prevac.gz
        /usr/bin/sudo -u postgres /usr/bin/vacuumdb --analyze itwishlist_postgresql_db
        /usr/bin/sudo -u postgres /usr/bin/pg_dump -Fc itwishlist_postgresql_db > /opt/backups/postvac.gz
        SCHEMA_BACKUP="/opt/backups/$(date +%w).db.schema"
        sudo -u postgres /usr/bin/pg_dump -C -s itwishlist_postgresql_db > $SCHEMA_BACKUP

        # or 

        cd /var/lib/pgsql/backups/
        su - postgres
        pg_dump -h localhost itwishlist_postgresql_db | gzip > /var/lib/pgsql/backups/itwishlist_postgresql_db_YYYY-MM-DD.gz

        # backups are stored in /var/lib/pgsql/backups

## Commands to Restart it.ippc.int and Related Software Upon Hardware Restart    {#hardwarerestart}

The following should be run automatically when the exlqaippc2.ext.fao.org (193.43.36.204) hardware restarts. I've put them in `/etc/rc.d/rc.local` on the server as per Unix sysadmin Johannes Glaser's recommendation:

**[Postgresql](http://www.postgresql.org/docs/9.0/static/server-start.html)** - the it.ippc.int database is called itwishlist_postgresql_db:

    su postgres -c '/usr/bin/postgres -D /usr/local/pgsql/data > logfile 2>&1 &'

**[Nginx](http://serverfault.com/a/213192)** - public facing web server - serves media and proxies dynamic requests to Gunicorn:

    service nginx start

**[Gunicorn](http://docs.gunicorn.org/en/latest/run.html)** - internal HTTP application server:

    cd /opt/projects/itwishlist-env && . bin/activate && cd itwishlist && gunicorn --daemon wsgi:application
    
    deactivate
    exit