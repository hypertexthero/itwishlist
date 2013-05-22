from itwishlist.apps.fileupload.models import File
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

# class FileMixin(object):
#     model = File
#     def get_success_url(self):
#         return reverse('upload-new')
#     # def get_queryset(self):
#     #     return File.objects.filter(owned_by=self.request.user)
# 
# class FileDetailView(FileMixin, DetailView):
#     pass

class FileDetailView(DetailView):
    model = File
    template_name = 'fileupload/file_detail.html'

class FileListView(ListView):
    model = File
    queryset = File.objects.all().order_by('-last_change')
    
    template_name = 'fileupload/file_list.html'

class FileCreateView(CreateView):
    model = File
    
    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "files/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "files/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(FileCreateView, self).get_context_data(**kwargs)
        context['files'] = File.objects.all()
        return context


class FileDeleteView(DeleteView):
    model = File

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/files/')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
