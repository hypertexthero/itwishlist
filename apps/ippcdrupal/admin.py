from ippcdrupal.models import *
from django.contrib import admin
from itwishlist.apps.ippcdrupal.models import DrupalUsers

class DrupalUsersAdmin(admin.ModelAdmin):
    save_on_top = True
    
admin.site.register(DrupalUsers, DrupalUsersAdmin)