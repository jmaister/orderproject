from django.contrib import admin

class EntityAdmin(admin.ModelAdmin):
    
    list_display = ("id", "name",)
    search_fields = ('name',)
    list_filter = ('name',)
    
    class Meta:
        abstract = True
