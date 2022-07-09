from django.contrib import admin

# Register your models here.
from .models import *


class TenantGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']


class TenantAdmin(admin.ModelAdmin):
    fields = ['pk', 'name', 'slug', 'group']


admin.site.register(TenantGroup, TenantGroupAdmin)
admin.site.register(Tenant, TenantAdmin)
