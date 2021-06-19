from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from map.managers import MarkerQuerySet


class Marker(models.Model):
    name = models.CharField(max_length=225, verbose_name=_('Title'))
    lng = models.DecimalField(max_digits=17, decimal_places=15, verbose_name=_('Longitude'))
    lat = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Latitude'))

    def __str__(self):
        return self.name

    objects = MarkerQuerySet.as_manager()

    class Meta:
        verbose_name = _('Marker')
        verbose_name_plural = _('Markers')


class MarkerImage(models.Model):
    marker = models.ForeignKey(to='Marker', on_delete=models.CASCADE, related_name='images')
    image = VersatileImageField(upload_to='images/', verbose_name=_('Image'))
    order = models.IntegerField(blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.order is None:
            self.order = self.marker.images.aggregate(max_order=Max('order')).get('max_order') or 0
            self.order += 1
        super().save(force_insert, force_update, using, update_fields)
