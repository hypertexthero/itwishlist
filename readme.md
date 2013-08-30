# IT Wish List

Naively-built website inspired by a well-known geek site to manage IT needs at work.

## Todo now

- [Allow logins from users with details in existing separate user database](http://hypertexthero.com/logbook/2013/08/identity-internet/)
    - <http://stackoverflow.com/questions/16482531/django-registration-custom-backend>
    - <http://stackoverflow.com/questions/18490696/authenticate-against-drupal-users-database-table-from-django-application>
    - <https://github.com/developmentseed/osso_relying>
    - <http://djangosnippets.org/snippets/2729/>
    - <https://github.com/evonove/django-oauth-toolkit>
    - <http://chirale.wordpress.com/2013/03/15/unified-login-in-django-and-drupal/>
    - <https://thenewcircle.com/s/post/1242/django_multiple_database_support>
    - <http://www.mail-archive.com/django-users@googlegroups.com/msg120598.html>
    - <https://docs.djangoproject.com/en/dev/topics/auth/customizing/>
    - <https://docs.djangoproject.com/en/1.3/howto/auth-remote-user/>
    - <http://djangosnippets.org/snippets/2777/>
    - <http://query7.com/django-authentication-backends>
    - <http://techydiary.com/how-to-handle-multiple-db-in-django/>
    - <http://stackoverflow.com/questions/12639830/django-authenticate-backend-multiple-databases>
    - <https://github.com/castlabs/django-cas>
- Refactor ranking algorythm using [the function from Drum](http://blog.jupo.org/2013/04/30/building-social-apps-with-mezzanine-drum/)

## Todo in Future (upcoming features)

- Rename URLS from 'post' to 'item'
- Port DB to MySQL for work setup
- Add [failed login blocker](https://github.com/alexkuhl/django-failedloginblocker) to mitigate brute-force attacks
- Set up fabric deployment
- Ability to vote on comments
- User karma system - users with karma above a certain threshold get new abilities such as downvotes
- Feeds & Content Export in Atom XML and JSON
- Previous/Next entry by user

[Some documentation is available](https://github.com/hypertexthero/itwishlist/tree/master/docs/documentation.md)