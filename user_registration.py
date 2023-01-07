import requests


class UserRegistration:
    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.user_email = None
        self.email_list = []
        self.first_name_list = []
        self.sheety_api = 'https://api.sheety.co/534704e14519d386a9d81a1f131dd383/flightDetails/users'
        self.bearer_token = AUTHORIZATION_TOKEN(if available)
        self.sheety_headers = {
            "Content-Type": "application/json",
            'Authorization': self.bearer_token
        }

    def take_credentials(self):
        print('Hey!!')
        self.firstName = input('First name:\n')
        self.lastName = input('Last name:\n')
        self.user_email = input('Your email\n')
        re_enter_email = input('Re-enter your email\n')

        while True:
            if self.user_email == re_enter_email:
                print(f'You are in {self.firstName}. Welcome to the cheap flight club!')
                break
            else:
                print('Oops!, emails are not matching')
                self.user_email = input('Your email\n')
                re_enter_email = input('Re-enter your email\n')

        sheety_json = {
            "user": {
                'firstName': self.firstName.title(),
                'lastName': self.lastName.title(),
                'email': self.user_email,
            }
        }

        response = requests.post(url=self.sheety_api, headers=self.sheety_headers, json=sheety_json)
        response.raise_for_status()

    def get_user_data(self):
        response = requests.get(url=self.sheety_api, headers=self.sheety_headers)
        response.raise_for_status()
        self.email_list = [data_dict['email'] for data_dict in response.json()['users']]
        self.first_name_list = [data_dict['firstName'] for data_dict in response.json()['users']]
        return self.email_list, self.first_name_list




