from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s[%d]' % (self.__class__.__name__, self.id or 0)

    def get_absolute_url(self):
        return '/%s/%d/' % (self.__class__.__name__, self.id)

    class Meta:
        abstract = True
        #ordering = ['created']


class BaseEntity(BaseModel):
    name = models.CharField(max_length=500, verbose_name=_('Name'))
    #active = models.BooleanField(default=True,editable=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%d/' % (self.__class__.__name__, self.id)

    class Meta:
        abstract = True
        ordering = ['name']
