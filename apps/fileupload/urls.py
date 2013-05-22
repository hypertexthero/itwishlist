from django.conf.urls.defaults import *
from itwishlist.apps.fileupload.views import FileCreateView, FileDeleteView, FileDetailView, FileListView

urlpatterns = patterns('',
    url(r'^upload/$', FileCreateView.as_view(), {}, 'upload-new'),
    url(r'^delete/(?P<pk>\d+)$', FileDeleteView.as_view(), {}, 'upload-delete'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$',
        view=FileDetailView.as_view(),
        name='upload-detail'),
    url(r'^$', FileListView.as_view(), {}, name='upload-list'),
)

