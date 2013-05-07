from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase

from datetime import datetime

# from imagekit.models.fields import ProcessedImageField
# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill
from easy_thumbnails.fields import ThumbnailerImageField

class Profile(ProfileBase):
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text="Your it.ippc.int byline.")
    email = models.EmailField(_("Email"), blank=True, help_text="An email address you want to display publically.")
    im = models.CharField(_("im"), max_length=50, null=True, blank=True, help_text="An instant messaging handle you want to display publically.")
    url = models.URLField(blank=True, null=True, help_text="A URL you may want to share?")
    remark = models.TextField(_("remark"), null=True, blank=True, help_text="Any remarks you would like to share?")
    user_photo = models.ImageField(_("Image"), upload_to="user_photo/%Y/%m/%d/", blank=True, help_text="Will be resized to 260x180 pixels, if larger.") # no player images yet
    # user_photo = ProcessedImageField(_("Image"), upload_to="user_photo/%Y/%m/%d/", blank=True) # no player images yet
    # player_thumb = ImageSpecField([ResizeToFill(260, 180)], format="JPEG", options={"quality": 75})
    date_joined = models.DateTimeField(_("Member Since"), default=datetime.now, editable=False)
    

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         # fields = ('name', 'player_id', 'email', 'im', 'remark',)
#         exclude = ("user_photo", "email",)