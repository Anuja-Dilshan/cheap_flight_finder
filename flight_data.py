import requests


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.location_api = 'https://api.tequila.kiwi.com/locations/query'
        self.tequila_api_key = API_KEY

        self.location_header = {
            'apikey': self.tequila_api_key,
            'accept': 'application/json'

        }
        self.location_params = {

            'term': '',
            'active_only': 'true',
        }

        # ______________________________________________________________________________________________________________

    def get_iata_codes(self, city_to_take_code: str) -> str:
        self.location_params['term'] = city_to_take_code
        response = requests.get(url=self.location_api, headers=self.location_header, params=self.location_params)
        response.raise_for_status()
        return response.json()['locations'][0]['code']
