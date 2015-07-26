import os
from django.db import models
from django.db.models import ImageField, FileField
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, time

#django tagging
#http://code.google.com/p/django-tagging/
from djangogallery.tagging.models import Tag
from djangogallery.tagging.fields import TagField

#threadlocals
#http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser
from djangogallery.middleware import threadlocals

## The Photo model
#
#  The model contains an ImageField to store the photo some informations on it and links to user and tags
class Photo(models.Model):
    #  The url of the image is determined by the date of today
    image = ImageField(upload_to="images/gallery/%Y/%b/%d", blank=False, null=False)
    #  a title
    title = models.CharField(max_length=75, blank=True)
    #  a caption
    caption = models.TextField(max_length=200, blank=True)

    #Default fkey as shown in http://code.djangoproject.com/ticket/6445
    author = models.ForeignKey(User, default=lambda: threadlocals.get_current_user().id)
    posted = models.DateTimeField(default=datetime.now)

    #  The associated tags
    tag = TagField(blank=True)

    def __unicode__(self):
        return self.id

    ## Redefined in a way that only the legitimate author can modify a photo
    def save(self):
        #only the author can edit
        if self.id and self.author == threadlocals.get_current_user():
            super(Photo, self).save()
        #the photo is new
        if not self.id:
            super(Photo, self).save()

    ## Redefined in a way that only the legitimate author can delete a photo
    def delete(self):
        #only the author can delete
        if self.author == threadlocals.get_current_user():
            filename=settings.MEDIA_ROOT+self.image
            if os.path.exists(filename):
                os.remove(filename)
            super(Photo, self).delete()

    class Admin:
        list_display = ('__unicode__', 'author', 'posted')
        list_per_page = 20

    class Meta:
        ordering = ('-posted',)
        get_latest_by = 'posted'