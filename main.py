from notification_manager import NotificationManager
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager


def if_user_want_to_add_city():
    user_city = input('What is the city to add to the search list: ').title()

    cur_data = DataManager().get_data()
    cur_city_list = [dictionary['city'] for dictionary in cur_data]
    if user_city in cur_city_list:
        print('you have already added that city')
    else:
        user_time_period = input('up to what date should we search for flights(format dd/mm/yyyy): ')
        DataManager().add_city(city_to_add=user_city, search_up_to=user_time_period)


def take_current_price():
    """if user want to know current price to a destination"""

    city = input('Your desired destination: ').title()
    print(f"the current price to {city} from CMB is ${DataManager().get_current_price(city_to_search=city)}")


def edit_existing_data():
    city = input('What is the name of the city that you like to edit?:  ').title()
    up_to = input('Up to which date should we search for flights to insert in your edited data(format dd/mm/yyyy): ')
    DataManager().edit_data(city=city, search_up_to=up_to)


def get_iata_code():
    """get IATA Code of any airport"""

    city = input('What is the name of the city').title()
    print(f"The IATA code of {city} is {FlightData().get_iata_codes(city_to_take_code=city)}")


DataManager().compare_price_and_notify(up_to_date=DATE)
