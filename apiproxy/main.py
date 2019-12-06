from typing import Tuple
import os
from json import dumps
from urllib.parse import urlparse, parse_qs, urlencode

from aiohttp import web, ClientSession
from aiohttp_swagger import setup_swagger


APP_ID = os.environ.get('LH_MAPS_APP_ID')
APP_CODE = os.environ.get('LH_MAPS_APP_CODE')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REACT_BUILD_PATH = os.environ.get(
    'LH_REACT_BUILD_PATH',
    os.path.join(BASE_DIR, '..', 'hotelmap', 'build')
)

routes = web.RouteTableDef()


@routes.view('/api/hotels/')
class HotelsView(web.View):
    search_distance = 10000

    # TODO: Add docstrings to methods
    def get_coords(self) -> Tuple[float]:
        """
        Get coordinates from GET parameters or raise an error
        in case they are missing or in wrong format.

        The format used is Decimal degrees
        """
        lat = self.request.query.get('lat', None)
        lon = self.request.query.get('lon', None)
        if not (lat and lon):
            raise web.HTTPException(text=dumps({'error': 'both lat and lon are required'}),
                                    content_type='application/json')

        try:
            lat, lon = map(float, [lat, lon])
        except ValueError:
            raise web.HTTPException(
                text=dumps({'error': 'Coordinates should be in float point format'}),
                content_type='application/json'
            )
        return lat, lon

    def build_url(self, lat: float, lon: float) -> str:
        """
        Build the URL for API request.

        Consider coordinates and pagination context
        """
        context = self.request.query.get('context', '')
        if context:
            context = f';context={context}'
        return (f'https://places.cit.api.here.com/places/v1/browse{context}'
                f'?app_id={APP_ID}'
                f'&app_code={APP_CODE}'
                f'&in={lat},{lon};r={self.search_distance}'
                f'&cat=accommodation')

    def convert_pagination_url(self, page_url: str) -> str:
        """
        Convert `next` and `previous` links to point to proxy server, not to Here API directly
        """
        parsed_url = urlparse(page_url)

        if 'context=' not in parsed_url.params:
            return page_url

        params = parse_qs(parsed_url.params)
        merged_params = dict(self.request.query)
        merged_params.update(context=params.get('context', ''))

        # We are running on Heroku, which sets this header.
        # Also we use it only for link building, so it should not be an issue
        scheme = self.request.headers.get('X-Forwarded-Proto', self.request.scheme)

        return (f'{scheme}://{self.request.host}{self.request.path}'
                f'?{urlencode(merged_params, doseq=True)}')

    def process_data(self, data: dict) -> dict:
        """
        This method does several changes with data, so format matches format from
        `apistored` application.

        1. Change the next and previous URLs to point to proxy
        2. Normalize first response and paginated response to have
           the same format
        3. Rename keys like `items` -> `results` to match DRF.
        """
        data = data.get('results', data)
        data['results'] = data.pop('items', [])
        for process_url in ('next', 'previous'):
            if process_url in data:
                data[process_url] = self.convert_pagination_url(data[process_url])
        return data

    async def get(self) -> web.Response:
        """
        Get Data from HERE maps API about accommodation places near selected point
        ---
        description: This end-point proxies lat&lon
                     to HERE Browse API to get hotels around
        tags:
        - Hotels
        produces:
        - application/json
        parameters:
        - in: query
          name: lat
          required: true
          description: Lattitude
          schema:
            format: float
            type: number
        - in: query
          name: lon
          required: true
          description: Longtitude
          schema:
            format: float
            type: number
        - in: query
          name: context
          required: false
          description: Context for pagination
          schema:
            type: string
        responses:
            "200":
                description: successful operation.
            "400":
                description: Invalid coordinates
        """
        lat, lon = self.get_coords()
        url = self.build_url(lat, lon)

        async with ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        data = self.process_data(data)

        return web.json_response(data)


def index_response(request):
    return web.FileResponse(os.path.join(REACT_BUILD_PATH, 'index.html'))


def _get_app():
    assert APP_CODE
    assert APP_ID

    app = web.Application()
    app.router.add_routes(routes)

    setup_swagger(
        app,
        description='Limehome Coding challenge. '
                    'https://gitlab.com/limehome/interviews/coding-challenge',
        title='Hotel Lookup API',
        contact='best.igor@gmail.com'
    )

    if os.path.exists(REACT_BUILD_PATH):
        app.router.add_get('/', index_response)
        app.router.add_static('/', REACT_BUILD_PATH, show_index=True)

    return app


if __name__ == '__main__':
    app = _get_app()
    web.run_app(app, port=int(os.environ.get('PORT', 8080)))
