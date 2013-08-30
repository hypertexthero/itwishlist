"""See https://docs.djangoproject.com/en/dev/topics/db/multi-db/#using-routers 
for details on db routers."""

class DrupalRouter(object): 
    """
    ippcdrupal/models.py => drupaldb
    others => default
    https://thenewcircle.com/s/post/1242/django_multiple_database_support
    """
    def db_for_read(self, model, **hints):
        "Point all read operations on ippcdrupal models to 'drupaldb'"
        if model._meta.app_label == 'ippcdrupal':
            return 'drupaldb'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all write operations on ippcdrupal models to 'drupaldb'"
        if model._meta.app_label == 'ippcdrupal':
            return 'drupaldb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in ippcdrupal app"
        if obj1._meta.app_label == 'ippcdrupal' and \
           obj2._meta.app_label == 'ippcdrupal':
            return True
        # Allow if neither is ippcdrupal app
        elif 'ippcdrupal' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'drupaldb' or model._meta.app_label == "ippcdrupal":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True
