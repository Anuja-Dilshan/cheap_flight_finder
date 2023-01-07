import requests
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_registration import UserRegistration
import time


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.city_list = ''
        self.sheety_api = 'https://api.sheety.co/534704e14519d386a9d81a1f131dd383/flightDetails/sheet1'
        self.bearer_token = 'Bearer dfgdfg45eergfdsfw4r3r23dwedwer34'
        self.sheety_headers = {
            "Content-Type": "application/json",
            'Authorization': self.bearer_token
        }

    def add_city(self, city_to_add: str, search_up_to: str):
        """parameters: city_to_add=(your destination), search_up_to=(Search flights for this city until this date)"""

        iata_code = FlightData().get_iata_codes(city_to_take_code=city_to_add)
        lowest_price = FlightSearch().flight_price(fly_to=city_to_add, up_to_date=search_up_to)

        if lowest_price is not None:
            sheety_json = {
                "sheet1": {
                    'city': city_to_add.title(),
                    'iataCode': iata_code,
                    'lowestPrice': lowest_price,
                }
            }
            response = requests.post(url=self.sheety_api, headers=self.sheety_headers, json=sheety_json)
            response.raise_for_status()
        else:
            print(f'Oops! no flights for {city_to_add} for given period ')

    def get_data(self) -> list:
        response = requests.get(url=self.sheety_api, headers=self.sheety_headers)
        response.raise_for_status()
        data_taken = response.json()
        return data_taken['sheet1']

    def get_current_price(self, city_to_search: str) -> str:
        data = self.get_data()
        city_list = [data_dict['city'] for data_dict in data]

        if city_to_search in city_list:
            return data[city_list.index(city_to_search)]['lowestPrice']
        else:
            x = input('Given destination is not included in your tracking list. '
                      'Do you like to include it?(yes/no): ').lower()
            if x == 'yes':
                up_to = input('Upto which date should we search for flights(format dd/mm/yyyy): ')
                self.add_city(city_to_add=city_to_search, search_up_to=up_to)
                time.sleep(5)
                return self.get_current_price(city_to_search=city_to_search)
            elif x == 'no':
                pass
            else:
                return 'invalid input'

    def edit_data(self, city: str, search_up_to: str):
        """:parameters: city=(name of the city to edit),
        search_up_to=(Search flights for this city until this date)"""

        data = self.get_data()
        city_list = [data_dict['city'] for data_dict in data]

        if city in city_list:
            iata_code = FlightData().get_iata_codes(city_to_take_code=city)
            lowest_price = FlightSearch().flight_price(fly_to=city, up_to_date=search_up_to)
            sheety_json = {
                "sheet1": {
                    'city': city,
                    'iataCode': iata_code,
                    'lowestPrice': lowest_price,
                }
            }
            sheety_api = f"{self.sheety_api}/{city_list.index(city) + 2}"
            response = requests.put(url=sheety_api, headers=self.sheety_headers, json=sheety_json)
            response.raise_for_status()
        else:
            user_say = input(f'{city} is not in your tracking list, do you like to enter it(yes/no): ').lower()
            if user_say == 'yes':

                self.add_city(city_to_add=city, search_up_to=search_up_to)
            elif user_say == 'no':
                pass
            else:
                print('invalid input')

    def compare_price_and_notify(self, up_to_date: str):
        """:parameter: up_to_date=(up to which date should search flights)"""

        for data_dict in self.get_data():

            cur_price_on_table = data_dict['lowestPrice']
            cur_city = data_dict['city']
            cur_city_iatacode = data_dict['iataCode']
            best_price_for_specified_period = FlightSearch().flight_price(fly_to=cur_city, up_to_date=up_to_date)
            if best_price_for_specified_period is not None:
                if best_price_for_specified_period < cur_price_on_table:
                    (email_list, name_list) = UserRegistration().get_user_data()
                    for num in range(len(email_list)):
                        msg = f'Subject:LOW PRICE ALERT!!\n\nHey {name_list[num]}\nonly ' \
                              f'${best_price_for_specified_period} to fly from ' \
                              f'Colombo-CMB to ' \
                              f'{cur_city}-{cur_city_iatacode}, from {FlightSearch().tomorrow} to {up_to_date} '
                        NotificationManager().send_email(msg=msg, email=email_list[num])
            else:
                print(f'Oops! No flights for {cur_city} in this time period')
