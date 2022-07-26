from django.contrib import admin

# Register your models here.
from .models import *


class TenantGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']

class TenantAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'group']

class SiteAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']

class LocationAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'site']


admin.site.register(TenantGroup, TenantGroupAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Location, LocationAdmin)
