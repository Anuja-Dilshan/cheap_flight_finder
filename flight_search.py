import requests
from flight_data import FlightData
from datetime import date, timedelta


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, ):
        self.tomorrow = (date.today() - timedelta(days=-1)).strftime('%d/%m/%Y')
        self.tequila_api = 'https://api.tequila.kiwi.com/v2/search'
        self.tequila_api_key = 'wpZf6A2jtJmw-su_0jV8FEr2Egy563tF'
        self.tequila_header = {
            'apikey': self.tequila_api_key,
            'Content - Type': 'application / json'
        }

    def flight_price(self, up_to_date: str, fly_to: str):
        """:parameters: up_to_date= upto which date you want to search flights,
        fly_to= your desired destination(dd/mm/yyyy format)"""

        tequila_params = {
            'fly_from': 'CMB',
            'fly_to': FlightData().get_iata_codes(city_to_take_code=fly_to),
            'date_from': self.tomorrow,
            'date_to': up_to_date,
            'curr': 'USD',
            'limit': 10,
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'one_for_city': 1

        }

        tequila_response = requests.get(url=self.tequila_api, params=tequila_params, headers=self.tequila_header)
        try:
            return tequila_response.json()['data'][0]['price']
        except IndexError:
            print(f'Oops! No flights for {fly_to} in this time period')
            return None



