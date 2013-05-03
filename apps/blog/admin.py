from django.contrib import admin

from itwishlist.apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'content_markdown')
    prepopulated_fields = { 'slug': ['title'] }

# class CategoryAdmin(admin.ModelAdmin):
# 	list_display = ('title', 'description')
# 	prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Post, PostAdmin)
# admin.site.register(Category, CategoryAdmin)
