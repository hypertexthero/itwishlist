# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

# http://stackoverflow.com/a/2683834/412329
import os.path

class File(models.Model):

    # This is a small demo using just two fields. The slug field is really not
    # necessary, but makes the code simpler. ImageField depends on PIL or
    # pillow (where Pillow is easily installable in a virtualenv. If you have
    # problems installing pillow, use a more generic FileField instead.

    file = models.FileField(upload_to="files/%Y/%m/", unique_for_date='last_change')
    # file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True, unique_for_date='last_change')
    # owned_by = models.ForeignKey(User, blank=True)
    last_change = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="added_files", verbose_name=('Uploaded by'))

    def __unicode__(self):
        return self.file.name

    def filename(self):
            return os.path.basename(self.file.name)

    # def owner(self):
    #     return [self.request.user]

    @models.permalink
    def get_absolute_url(self):
        # return ('upload-detail', args=[self.pk])
        # return ('upload-detail', )
        return ('upload-detail', (), {
                            'id': self.id,
                            # 'year': self.last_change.strftime("%Y"),
                            # 'month': self.last_change.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'slug': self.slug})

    def save(self, *args, **kwargs):
        self.id = self.id
        self.slug = self.file.name
        # self.uploaded_by = self.request.user
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.file.name)
        self.last_change = datetime.datetime.now()
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(File, self).delete(*args, **kwargs)
