from datetime import date, timedelta
from urllib.parse import urlencode

from celery import shared_task, Task
from django.contrib.gis.geos import Point
from django.conf import settings
import requests

from .models import Hotel

fetch_hotels: Task


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
    params = {
        'app_id': settings.APP_ID,
        'app_code': settings.APP_CODE,
        'in': f'{lat},{lon};r=10000',
        'cat': 'accommodation',
        'size': '100',
    }
    url = (f'https://places.cit.api.here.com/places/v1/browse'
           f'?{urlencode(params)}')

    while url and pages:
        results = data = requests.get(url).json()

        if 'results' in data:
            # Difference between first and next pages
            results = data['results']

        store_data(results['items'])

        pages -= 1
        url = results.get('next')


@shared_task
def clean_up_hotels():
    # find hotels that were not requested for a while
    update_edge = date.today() - timedelta(days=90)
    old_hotels = (Hotel.objects
                  .filter(last_update__lt=update_edge)
                  .order_by('last_update'))

    # Process up to 100
    for hotel in old_hotels:
        params = {
            'app_id': settings.APP_ID,
            'app_code': settings.APP_CODE,
            'source': 'sharing',
            'id': hotel.api_id,
        }
        url = (f'https://places.cit.api.here.com/places/v1/places/lookup'
               f'?{urlencode(params)}')

        response = requests.get(url)

        if not response.ok and response.status_code == 404:
            hotel.delete()
            continue

        data = response.json()
        hotel.title = data.get('name', hotel.title)
        hotel.save()
