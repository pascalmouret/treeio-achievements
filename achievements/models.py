"""
This module only needs two simple models, Prototype being the "raw" Achievements and while
the objects called Achievements are only a connection of a Prototype and a tree.io-User
Also, because this is tree.io, the models inherit from Object, a class which is responsible for
access, notifications, likes and so on.
"""
from django.db import models
from django.utils.html import strip_tags
from treeio.core.models import User, Object


class Prototype(Object):
    """ A raw Achievement that is used as a reference to avoid redundancy. """
    title = models.CharField(max_length=255, unique=True)
    text = models.CharField(max_length=512)
    badge = models.ImageField(upload_to='achievements-badges', blank=True)
    icon = models.ImageField(upload_to='achievements-icons', blank=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        """ Added the [Prototype] in order not to confuse Achievements and Prototypes """
        return '%s [Prototype]' % self.title

    @property
    def summary(self):
        """ Used for the Prototypes-list to pack it into one line """
        return strip_tags(self.text[:100])

    @property
    def name(self):
        """ A tree.io templatetag can sort lists alphabetically by the name attribute. """
        return self.title


class Achievement(Object):
    """ A entity used to give an Achievement to a user. """
    prototype = models.ForeignKey(Prototype)
    user = models.ForeignKey(User, related_name='achievements')
    text = models.CharField(max_length=512, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        """ Added name of user, since Achievements can be given to multiple users. """
        return '%s [%s]' % (self.prototype.title, self.user.get_username())

    @property
    def name(self):
        """ A tree.io templatetag can sort lists alphabetically by the name attribute. """
        return self.prototype.title
