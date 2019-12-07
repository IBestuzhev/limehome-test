from datetime import date, timedelta
from urllib.parse import urlencode
import logging

from celery import shared_task, Task
from django.contrib.gis.geos import Point
from django.conf import settings
import requests

from .models import Hotel


logger = logging.getLogger(__name__)
fetch_hotels: Task
clean_up_hotels: Task


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
def fetch_hotels(lat: float, lon: float, pages: int = 5, radius: int = 10000):
    """
    Downloads data from Here API and store it into DB.

    It uses `/browse` API to download list of places with `accommodation` type.
    `lat`, `lon` and `radius` are used to specify search area.

    This task downloads up to `pages` pages, 100 elements on each.
    """
    params = {
        'app_id': settings.APP_ID,
        'app_code': settings.APP_CODE,
        'in': f'{lat},{lon};r={radius}',
        'cat': 'accommodation',
        'size': '100',
    }
    url = (f'https://places.cit.api.here.com/places/v1/browse'
           f'?{urlencode(params)}')

    logger.info(f'Fetching data for {lat}, {lon}')

    while url and pages:
        logger.debug(f'Downloading {url}')
        response = requests.get(url)

        if not response.ok:
            logger.error(f'Error {response.status_code} on URL: {url}')
            return

        results = data = response.json()

        if 'results' in data:
            # Difference between first and next pages
            results = data['results']

        store_data(results['items'])

        pages -= 1
        url = results.get('next')


@shared_task
def clean_up_hotels():
    """
    Task that should be launched periodicaly.

    It looks for hotels that were not downloaded from API for a while.
    Either nobody looked at that aread, or this hotel was deleted.

    This task uses `/lookup` API to check if hotel still exists on Here Maps.
    """
    # find hotels that were not requested for a while
    update_edge = date.today() - timedelta(days=90)
    old_hotels = (Hotel.objects
                  .filter(last_update__lt=update_edge)
                  .order_by('last_update'))

    logger.info(f'There are {old_hotels.count()} obsolete hotels')

    # Process up to 100
    for hotel in old_hotels[:100].iterator():
        params = {
            'app_id': settings.APP_ID,
            'app_code': settings.APP_CODE,
            'source': 'sharing',
            'id': hotel.api_id,
        }
        url = (f'https://places.cit.api.here.com/places/v1/places/lookup'
               f'?{urlencode(params)}')

        logger.debug(f'Download hotel info for {hotel.api_id}')

        response = requests.get(url)

        if not response.ok and response.status_code == 404:
            logger.debug(f'Deleting hotel with {hotel.api_id}')
            hotel.delete()
            continue
        elif not response.ok:
            logger.error(f'Error {response.status_code} on URL: {url}')
            continue

        data = response.json()
        hotel.title = data.get('name', hotel.title)
        hotel.save()
        logger.debug(f'Hotel with id={hotel.api_id} was updated.')
