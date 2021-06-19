from decimal import Decimal

from django.db.models import F
from django.db.models import QuerySet
from django.db.models.functions import Power, Sin, Cos, ATan2, Sqrt, Radians


class MarkerQuerySet(QuerySet):
    def closest(self, latitude, longitude, max_distance=5):
        latitude = Decimal(latitude)
        longitude = Decimal(longitude)
        dlat = Radians(F('lat') - latitude)
        dlong = Radians(F('lng') - longitude)

        a = (
                Power(Sin(dlat / 2), 2) + Cos(Radians(latitude))
                * Cos(Radians(F('lat'))) * Power(Sin(dlong / 2), 2)
        )

        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))

        return self.annotate(
            distance=6371 * c
        )
