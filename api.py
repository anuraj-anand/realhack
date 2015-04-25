import requests


str_join = lambda _c, _a: _c.join(map(str, _a))
list_join = lambda _i: str_join('|', _i)
url_join = lambda _a: str_join('/', _a)


class ResponseParser():

    @staticmethod
    def parse_coords(result):
        geometry = result['geometry']
        location = geometry['location']
        lat = location['lat']
        lng = location['lng']
        coords = str_join(',', (lat, lng))

        return coords


class GoogleMapsAPI():

    try:
        with open('key.env', 'r') as f:
            API_KEY = f.read().strip()
    except:
        raise RuntimeError('API Keyfile missing!')

    API_URL = 'https://maps.googleapis.com/maps/api'

    ENDPOINT = ''

    RESPONSE_TYPE = 'json'  # or 'xml'

    MAX_RADIUS = '1000'  # meters

    @classmethod
    def request(cls, payload, service=''):
        if service:
            postfix = url_join((service, cls.RESPONSE_TYPE))
        else:
            postfix = cls.RESPONSE_TYPE
        url = url_join((cls.API_URL, cls.ENDPOINT, postfix))

        payload['key'] = cls.API_KEY

        response = requests.get(url, params=payload)
        json_response = response.json()

        return json_response


class GeocodeAPI(GoogleMapsAPI):

    ENDPOINT = 'geocode'

    @classmethod
    def get_coords(cls, place_name):
        response = cls.request({
            'address': place_name,
        })
        results = response['results']

        result = results[0]
        coords = ResponseParser.parse_coords(result)

        return coords


class DistanceMatrixAPI(GoogleMapsAPI):

    ENDPOINT = 'distancematrix'

    @classmethod
    def get_distance_matrix_between(cls, source_name, destination_name):
        response = cls.request({
            'origins': source_name,
            'destinations': destination_name,
        })
        rows = response['rows']

        return rows

    @classmethod
    def get_distance_matrix_between_multiple(cls, sources, destinations):
        return cls.get_distance_matrix_between(
            *map(list_join, (sources, destinations))
        )


class PlacesAPI(GoogleMapsAPI):

    ENDPOINT = 'place'

    @classmethod
    def nearby_search(cls, place_name, nearby_type):
        place_coords = GeocodeAPI.get_coords(place_name)

        response = cls.request(
            {
                'location': place_coords,
                'radius': cls.MAX_RADIUS,
                'types': nearby_type,
            },
            'nearbysearch'
        )
        results = response['results']

        return results

    @classmethod
    def text_search(cls, place_name, nearby_type, text):
        place_coords = GeocodeAPI.get_coords(place_name)

        response = cls.request(
            {
                'location': place_coords,
                'radius': cls.MAX_RADIUS,
                'query': text,
                'types': nearby_type,
            },
            'textsearch'
        )
        results = response['results']

        return results
