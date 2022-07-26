from django.db import models
from django.urls import reverse

__all__ = [
    'Site',
    'Location',
]

#
# Site
#
class Site(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dcim:site', args=[self.id])

#
# Locations
#
class Location(models.Model):
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        max_length=100
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='locations'
    )

    class Meta:
        ordering = ['site', 'name']
        constraints = (
            models.UniqueConstraint(
                fields=('site', 'name'),
                name='dcim_location_name',
            ),
            models.UniqueConstraint(
                fields=('site', 'slug'),
                name='dcim_location_slug',
            ),
        )

    def get_absolute_url(self):
        return reverse('dcim:location', args=[self.pk])

    # def validate_unique(self, exclude=None):
    #     locations = Location.objects.exclude(pk=self.pk)
    #     if locations.filter(name=self.name, site=self.site).exists():
    #         raise ValidationError({
    #             "name": f"A location with this name in site {self.site} already exists."
    #         })
    #     if locations.filter(slug=self.slug, site=self.site).exists():
    #         raise ValidationError({
    #             "name": f"A location with this slug in site {self.site} already exists."
    #         })
