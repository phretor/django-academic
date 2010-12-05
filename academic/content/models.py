from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from filebrowser.fields import FileBrowseField
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
except:
    pass

class Download(models.Model):
    class Meta:
        ordering = [
            'title', ]
    
    title = models.CharField(
        max_length=256)
    description = models.TextField(
        blank=True,
        null=True)
    file = FileBrowseField(
        _('File'),
        max_length=256,
        format='Document',
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s%s' % (self.title, self.file)
