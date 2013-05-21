from django.contrib import admin

from itwishlist.apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'publish', 'status', 'author')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'content_markdown')
    prepopulated_fields = { 'slug': ['title'] }

# class CategoryAdmin(admin.ModelAdmin):
# 	list_display = ('title', 'description')
# 	prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Post, PostAdmin)
# admin.site.register(Category, CategoryAdmin)
