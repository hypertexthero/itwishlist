from django.contrib import admin

from .models import File

class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'slug', 'last_change')
    # list_filter = ('publish', 'status', 'author')
    search_fields = ('file', 'slug')
    # prepopulated_fields = { 'slug': ['title'] }

admin.site.register(File, FileAdmin)
