from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from .serializers import HotelSerializer, CoordinatesSerializer
from .models import Hotel, GeoQueryset
from .tasks import fetch_hotels


class HotelDistancePagination(CursorPagination):
    ordering = 'distance'
    page_size = 20

    def _get_position_from_instance(self, instance, ordering):
        return instance.distance.m


class HotelList(ListAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    pagination_class = HotelDistancePagination

    # TODO: Explain this configuration
    fetch_sync = False
    fetch_async = False
    fetch_threshold = None

    def pre_fetch_coords(self, point: Point):
        # TODO: Write bout this hooks
        if self.fetch_sync:
            fetch_hotels(point.y, point.x)

        if self.fetch_async:
            fetch_hotels.delay(point.y, point.x)

    def post_fetch_coords(self, point: Point, queryset: GeoQueryset):
        if self.fetch_threshold and queryset.count() < self.fetch_threshold:
            fetch_hotels.delay(point.y, point.x)

    def get_queryset(self):
        coordinates_serializer = CoordinatesSerializer(data=self.request.query_params)
        coordinates_serializer.is_valid(raise_exception=True)

        point = coordinates_serializer.validated_data['point']

        self.pre_fetch_coords(point)

        queryset: GeoQueryset = super().get_queryset()
        queryset = queryset.calculate_distance(point)
        queryset = queryset.filter_by_distance(D(km=2))
        queryset = queryset.order_by('distance')

        self.post_fetch_coords(point, queryset)

        return queryset
