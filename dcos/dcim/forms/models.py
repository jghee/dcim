from django import forms

from dcim.models import *


class TenantGroupForm(forms.ModelForm):
    class Meta:
        model = TenantGroup
        fields = ['name', 'slug']


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'group']
