from django.test import TestCase, RequestFactory
from unittest import mock
from django.contrib.gis.geos import Point

from .models import Hotel
from .views import HotelList

# Create your tests here.


@mock.patch('hotels.views.fetch_hotels')
class FetchTaskTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_pre_sync(self, mocked_task: mock.MagicMock):
        """
        In this mode sync task is always called before fetching data from DB.
        This makes request slow, but always show actual data
        """
        view = HotelList.as_view(
            fetch_sync=True,
            fetch_async=False,
            fetch_threshold=None
        )
        request = self.factory.get('/api/hotels/?lat=10&lon=10')
        view(request)

        mocked_task.assert_called_once_with(10., 10., 1, radius=10000)
        mocked_task.delay.assert_not_called()

    def test_post_sync(self, mocked_task: mock.MagicMock):
        """
        In this mode task is always called via celery
        This keeps list of places in sync
        But user in request gets older data from DB
        """
        view = HotelList.as_view(
            fetch_sync=False,
            fetch_async=True,
            fetch_threshold=None
        )
        request = self.factory.get('/api/hotels/?lat=10&lon=10')
        view(request)

        mocked_task.delay.assert_called_once_with(10., 10., radius=10000)
        mocked_task.assert_not_called()

    def _run_threshold_test(self, amount: int = 5):
        """
        Helper method to create some hotels before running the test
        """
        view = HotelList.as_view(
            fetch_sync=False,
            fetch_async=False,
            fetch_threshold=5
        )
        hotels = [
            Hotel(
                position=Point(10 + i / 10000, 10 + i / 10000, srid=4326),  # WGS 84
                title=f'Hotel {i}',
                api_id=f'id-{i}'
            )
            for i in range(1, amount)
        ]
        Hotel.objects.bulk_create(hotels)

        request = self.factory.get('/api/hotels/?lat=10&lon=10')
        view(request)

    def test_threshold_sync(self, mocked_task: mock.MagicMock):
        """
        Threshold mode - run sync task only if there are less then ``fetch_threshold``
        items in the database
        """
        self._run_threshold_test(5)

        mocked_task.delay.assert_called_once_with(10., 10., radius=10000)
        mocked_task.assert_not_called()

    def test_over_threshold(self, mocked_task: mock.MagicMock):
        """
        Threshold test when we have enough data in DB. No task is called
        """
        self._run_threshold_test(10)

        mocked_task.assert_not_called()
        mocked_task.delay.assert_not_called()


class DistanceSortTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Hotel.objects.bulk_create([
            # The closest hotel
            Hotel(title='closest',
                  position=Point(10.01, 10., srid=4326),
                  api_id='h1'),
            # Away, but inside search radius
            Hotel(title='away',
                  position=Point(10.05, 10., srid=4326),
                  api_id='h2'),
            # Outside search radius
            Hotel(title='far away',
                  position=Point(15., 40., srid=4326),
                  api_id='h3'),
        ])

    def test_distance_search(self):
        view = HotelList.as_view(
            fetch_sync=False,
            fetch_async=False,
            fetch_threshold=None,
        )
        request = self.factory.get('/api/hotels/?lat=10&lon=10')
        response = view(request)

        self.assertEqual(len(response.data['results']), 2)
        hotels = [d['title'] for d in response.data['results']]
        self.assertEqual(hotels, ['closest', 'away'])
