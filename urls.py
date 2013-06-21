from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.date_based import archive_index
from itwishlist.apps.blog import views
from django.contrib import admin
admin.autodiscover()
from pinax.apps.account.openid_consumer import PinaxConsumer

handler500 = "pinax.views.server_error"

from itwishlist.apps.blog.feeds import BlogFeedUser
blogs_feed_dict = {"feed_dict": {
    'only': BlogFeedUser,
    }}

from itwishlist.apps.blog.models import Post, IS_PUBLIC
post_dict_public = {
    'queryset': Post.objects.filter(status=IS_PUBLIC),
    'template_object_name': 'post',
}
post_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
}

# =todo: vanity url: http://stackoverflow.com/questions/3333765/get-user-from-url-segment-with-django 

urlpatterns = patterns("",

    url(r"^$", "itwishlist.apps.blog.views.homepage", name="home"),
    url(r"^new/$", "itwishlist.apps.blog.views.new", name="new"),

    url(r"^bug/$", "itwishlist.apps.blog.views.bug", name="bug"),
    url(r"^feature/$", "itwishlist.apps.blog.views.feature", name="feature"),
    url(r"^done/$", "itwishlist.apps.blog.views.done", name="done"),
    url(r"^inprogress/$", "itwishlist.apps.blog.views.inprogress", name="inprogress"),
    url(r"^kb/$", "itwishlist.apps.blog.views.kb", name="kb"),
    
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    # url(r"^about/", include("about.urls")),
    url(r"^faq/$", direct_to_template, {"template": "faq.html"}, name="faq"),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("profiles.urls")), # NOTA BENE: that this is pointing to profiles/urls.py and not IDIOS app...
    # url(r"^up/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    # url(r'^log/', include('blog.urls')),
    url(r'^posts/', include('itwishlist.apps.blog.urls')),
    url(r'^relationships/', include('relationships.urls')),
    url(r'^following/','itwishlist.apps.blog.views.following', name='following'),
    url(r'^followers/','itwishlist.apps.blog.views.followers', name='followers'),
    url(r'^backup/$', 'itwishlist.apps.blog.views.backup', name='backup'),
    url(r'^desk/$', 'itwishlist.apps.blog.views.desk', dict(post_dict, template_name='blog/desk.html'), name='desk'),
    url(r'^post/$', 'itwishlist.apps.blog.views.add', name='blog_add'),
    # url(r'^b/', include('blogs.short_urls')), # For short urls, if you want
    url(r'^feeds/posts/(?P<url>w+)/', 'django.contrib.syndication.views.feed', blogs_feed_dict),
    url(r'^search/$', 'itwishlist.apps.blog.views.search', name="search"),
    url(r'^files/', include('itwishlist.apps.fileupload.urls')),
    )

# urlpatterns += patterns('django.views.generic.simple',
#     url(r'^about/$', 'direct_to_template', {'template': 'about.html'}, name='about'),
# )


# if settings.SERVE_MEDIA:
#     urlpatterns += patterns("",
#         url(r"", include("staticfiles.urls")),
#     )

# =todo: figure out why I had to add this so player image is served
if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )