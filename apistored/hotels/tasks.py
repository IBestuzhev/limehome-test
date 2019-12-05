from celery import shared_task, Task
from django.contrib.gis.geos import Point
import requests

from .models import Hotel

fetch_hotels: Task
# TODO: load from environ
APP_ID = 'Tbu3xBVyM9dUB0HlkAfi'
APP_CODE = '96rvfoL4yKT9u9d79F8jag'


def store_data(hotels):
    for hotel in hotels:
        Hotel.objects.update_or_create(
            api_id=hotel['id'],
            defaults=dict(
                title=hotel['title'],
                position=Point(hotel['position'][1], hotel['position'][0]),
                icon=hotel['icon']
            )
        )


@shared_task
def fetch_hotels(lat: float, lon: float, pages: int = 5):
    url = (f'https://places.cit.api.here.com/places/v1/browse'
           f'?app_id={APP_ID}'
           f'&app_code={APP_CODE}'
           f'&in={lat},{lon};r=10000'
           f'&cat=accommodation'
           f'&size=100')

    while url and pages:
        results = data = requests.get(url).json()

        if 'results' in data:
            # Difference between first and next pages
            results = data['results']

        store_data(results['items'])

        pages -= 1
        url = results.get('next')

# TODO: Cleanup task - check last_updated and try to get via ID
