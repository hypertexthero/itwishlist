# -*- coding: utf-8 -*-
from django import forms
from apps.fileupload.models import File

# class AlbumForm(forms.ModelForm):
# 
#     class Meta:
#         model = Album
#         fields = ['title', 'is_public']

class FileUploadForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file']