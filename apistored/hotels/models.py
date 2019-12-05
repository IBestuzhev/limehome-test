from typing import List

from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance as DistanceType
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class GeoQueryset(models.QuerySet):
    def calculate_distance(self, point: Point) -> 'GeoQueryset':
        return self.annotate(distance=Distance('position', point))

    def filter_by_distance(self, point: Point, distance: DistanceType) -> 'GeoQueryset':
        return self.filter(position__distance_lte=(point, distance))


class Hotel(models.Model):
    title = models.CharField(max_length=250)
    position = models.PointField(geography=True)
    icon = models.URLField(blank=True)
    api_id = models.CharField(max_length=50, db_index=True, unique=True)

    last_update = models.DateField(auto_now=True)

    objects = GeoQueryset.as_manager()

    def __str__(self):
        return self.title

    def reversed_coords(self) -> List[float]:
        # Lat first
        return self.position.coords[::-1]
