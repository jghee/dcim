from django.db import models
from django.urls import reverse

__all__ = (
    'Tenant',
    'TenantGroup',
)


class TenantGroup(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('dcim:tenantgroup', args=[self.pk])


class Tenant(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )
    group = models.ForeignKey(
        to='dcim.TenantGroup',
        on_delete=models.SET_NULL,
        related_name='tenants',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dcim:tenant', args=[self.pk])
