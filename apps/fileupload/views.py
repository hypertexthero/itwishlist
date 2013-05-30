import datetime

from itwishlist.apps.fileupload.models import File
from itwishlist.apps.fileupload.forms import FileUploadForm

from django.views.generic import CreateView, DeleteView, DetailView, ListView

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.conf import settings

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class LoginRequiredMixin(object):
    """ View mixin which verifies that the user has authenticated. """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

# class FileMixin(object):
#     model = File
#     def get_success_url(self):
#         return reverse('upload-new')
#     def get_queryset(self):
#         return File.objects.filter(uploaded_by=self.request.user)
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


class FileCreateView(LoginRequiredMixin, CreateView):

    model = File
    form_class = FileUploadForm        

    def get_context_data(self, **kwargs):
        context = super(FileCreateView, self).get_context_data(**kwargs)
        context['files'] = File.objects.all()
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploaded_by = self.request.user
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 
                 'fileurl': settings.MEDIA_URL + "files/" +
                    self.object.last_change.strftime("%Y/%m") + "/" + self.object.filename(), 
                 # 'fileurl': reverse('upload-file-detail', args=[self.object.slug]),
                 # 'uploaded_by': f.uploaded_by,
                 'sitename': settings.SITE_NAME,
                 'url': reverse('upload-detail', args=[self.object.id, self.object.slug]), 
                 # 'thumbnail_url': settings.MEDIA_URL + "files/" + f.name.replace(" ", "_"), 
                 'delete_url': reverse('upload-delete', args=[self.object.id]), 
                 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    
    # def form_invalid(self, form):
    #     print form
    #     return super(FileCreateView, self).form_invalid(form)
            
    # def dispatch(self, request, *args, **kwargs):
    #     self.file = get_object_or_404(File)
    #     if self.file.uploaded_by == request.user:
    #         return super(FileCreateView, self).dispatch(request, *args, **kwargs)
    #     raise PermissionDenied


class FileDeleteView(DeleteView):
    model = File

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        # http://stackoverflow.com/a/5532445/412329
        self.object = self.get_object()
        if not self.object.uploaded_by == self.request.user:
            raise PermissionDenied
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, message=("Successfully deleted file."))
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
