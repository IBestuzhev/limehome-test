from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.geos import Point

from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True, source='distance.m')
    position = serializers.ListField(read_only=True, child=serializers.FloatField(),
                                     source='reversed_coords')

    class Meta:
        model = Hotel
        fields = ['distance', 'position', 'title', 'icon', 'id']


class CoordinatesSerializer(serializers.Serializer):
    lat = serializers.FloatField(required=True,
                                 validators=[MaxValueValidator(90.), MinValueValidator(-90.)])
    lon = serializers.FloatField(required=True,
                                 validators=[MaxValueValidator(180.), MinValueValidator(-180.)])

    def validate(self, data):
        data['point'] = Point(data['lon'], data['lat'], srid=4326)  # WGS 84
        return data
