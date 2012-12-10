from django.db import models

class BaseModel(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        # return '%s[%d]' % (__class__, self.id)
        return '[%d]' % (self.id)

    def get_absolute_url(self):
        return '/%s/%d/' % (__class__, self.id)

    class Meta:
        abstract = True
        #ordering = ['created']

class BaseEntity(BaseModel):
    name = models.CharField(max_length=500)
    #active = models.BooleanField(default=True,editable=False)
      
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%d/' % (__class__, self.id)

    class Meta:
        abstract = True
        ordering = ['name']
