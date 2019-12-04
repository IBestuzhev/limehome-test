from typing import Tuple
from json import dumps
from urllib.parse import urlparse, parse_qs, urlencode

from aiohttp import web, ClientSession
from aiohttp_swagger import setup_swagger


# TODO: load from environ
APP_ID = 'Tbu3xBVyM9dUB0HlkAfi'
APP_CODE = '96rvfoL4yKT9u9d79F8jag'


routes = web.RouteTableDef()


@routes.view('/api/hotels/')
class HotelsView(web.View):
    # TODO: Add docstrings to methods
    def get_coords(self) -> Tuple[float]:
        lat = self.request.query.get('lat', None)
        lon = self.request.query.get('lon', None)
        if not (lat and lon):
            raise web.HTTPException(text=dumps({'error': 'both lat and lon are required'}),
                                    content_type='application/json')
            return web.json_response({'error': 'both lat and lon are required'},
                                     status=400)

        try:
            lat, lon = map(float, [lat, lon])
        except ValueError:
            raise web.HTTPException(
                text=dumps({'error': 'Coordinates should be in float point format'}),
                content_type='application/json'
            )
            return web.json_response(
                {'error': 'Coordinates should be in float point format'},
                status=400
            )
        return lat, lon

    def build_url(self, lat: float, lon: float) -> str:
        context = self.request.query.get('context', '')
        if context:
            context = f';context={context}'
        return (f'https://places.cit.api.here.com/places/v1/browse{context}'
                f'?app_id={APP_ID}'
                f'&app_code={APP_CODE}'
                f'&in={lat},{lon};r=2000'
                f'&cat=accommodation')

    def convert_pagination_url(self, page_url: str) -> str:
        parsed_url = urlparse(page_url)

        if 'context=' not in parsed_url.params:
            return page_url

        params = parse_qs(parsed_url.params)
        merged_params = dict(self.request.query)
        merged_params.update(context=params.get('context', ''))

        return (f'{self.request.scheme}://{self.request.host}{self.request.path}'
                f'?{urlencode(merged_params, doseq=True)}')

    def process_data(self, data: dict) -> dict:
        # TODO: Describe reasons for this transformation
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


if __name__ == '__main__':
    app = web.Application()
    app.router.add_routes(routes)

    setup_swagger(
        app,
        description='Limehome Coding challenge. '
                    'https://gitlab.com/limehome/interviews/coding-challenge',
        title='Hotel Lookup API',
        contact='best.igor@gmail.com'
    )

    # TODO: Load port from environ
    web.run_app(app)
