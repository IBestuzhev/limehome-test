from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from .serializers import HotelSerializer, CoordinatesSerializer
from .models import Hotel, GeoQueryset
from .tasks import fetch_hotels


class HotelDistancePagination(CursorPagination):
    ordering = 'distance'
    page_size = 20

    def _get_position_from_instance(self, instance, ordering):
        return instance.distance.m


@method_decorator(swagger_auto_schema(query_serializer=CoordinatesSerializer), name='get')
class HotelList(ListAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    pagination_class = HotelDistancePagination
    search_distance = 10000

    # I think this is not ready for production, but OK for coding challenge
    # In real-life project I would expect another way to populate DB, like speical API
    # to import it completely
    # Or if this approach is used there should be a system to truncate coords
    # and store log to rate-limit querys for single area.

    # However coding challenge works with HERE API and fetch small pieces of data.
    # So there are several modes how to populate DB
    # More description is in `hotels/tests.py`

    # Run Here map API syncronously before checking the DB
    fetch_sync = True
    # Call API ayncronously with the same coordinates
    # Return data to user immediately from DB
    # Later data is refreshed
    fetch_async = False
    # Call API only if we have less then fetch_threshold results
    fetch_threshold = None

    def pre_fetch_coords(self, point: Point):
        """
        Hook to fetch data from Here API *before* querying the DB.
        """
        if 'cursor' in self.request.query_params:
            return
        if self.fetch_sync:
            fetch_hotels(point.y, point.x, 1, radius=self.search_distance)

        if self.fetch_async:
            fetch_hotels.delay(point.y, point.x, radius=self.search_distance)

    def post_fetch_coords(self, point: Point, queryset: GeoQueryset):
        """
        Hook after database query is executed.

        If DB returned less values than `fetch_threshold` it creates celery task
        to fetch more data for selected area.

        Does not run on 2+ pages
        """
        if 'cursor' in self.request.query_params:
            return

        if self.fetch_threshold and queryset.count() < self.fetch_threshold:
            fetch_hotels.delay(point.y, point.x, radius=self.search_distance)

    def get_queryset(self):
        coordinates_serializer = CoordinatesSerializer(data=self.request.query_params)
        coordinates_serializer.is_valid(raise_exception=True)

        point = coordinates_serializer.validated_data['point']

        self.pre_fetch_coords(point)

        queryset: GeoQueryset = super().get_queryset()
        queryset = queryset.filter_by_distance(point, D(m=self.search_distance))
        queryset = queryset.calculate_distance(point)
        queryset = queryset.order_by('distance')

        self.post_fetch_coords(point, queryset)

        return queryset
